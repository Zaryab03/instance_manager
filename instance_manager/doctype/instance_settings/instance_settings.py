# Copyright (c) 2026, Your Organization
# License: MIT

import frappe
from datetime import date

from frappe.model.document import Document


class InstanceSettings(Document):
	"""Instance Settings DocType for managing instance limits and expiry"""

	def validate(self):
		"""Validate instance settings"""
		if self.ess_user_limit < 0:
			frappe.throw("ESS User Limit cannot be negative")
		
		if self.core_user_limit < 0:
			frappe.throw("Core User Limit cannot be negative")
		
		if self.database_limit_gb <= 0:
			frappe.throw("Database Limit must be greater than 0")
		
		if self.expiry_date and self.expiry_date < date.today():
			frappe.msgprint("Warning: Expiry date is in the past!", alert=True)

	def on_update(self):
		"""Update status information"""
		self.update_status_info()

	def update_status_info(self):
		"""Update the HTML status information"""
		days_left = self.get_days_remaining()
		ess_count = self.get_ess_user_count()
		core_count = self.get_core_user_count()
		
		status_html = f"""
		<div class="instance-status-info">
			<p><strong>ESS Users:</strong> {ess_count} / {self.ess_user_limit}</p>
			<p><strong>Core Users:</strong> {core_count} / {self.core_user_limit}</p>
			<p><strong>Days Remaining:</strong> {days_left} days</p>
		</div>
		"""
		self.status_info = status_html

	def get_days_remaining(self):
		"""Calculate days remaining until expiry"""
		if not self.expiry_date:
			return -1
		
		days = (self.expiry_date - date.today()).days
		return max(days, 0)

	def get_ess_user_count(self):
		"""Get count of active ESS users"""
		return frappe.db.count("User", filters={
			"enabled": 1,
			"user_type": "Website User"
		})

	def get_core_user_count(self):
		"""Get count of active core (system) users"""
		return frappe.db.count("User", filters={
			"enabled": 1,
			"user_type": "System User"
		})

	@staticmethod
	def get_instance_settings():
		"""Get or create the instance settings document"""
		try:
			return frappe.get_doc("Instance Settings", "Instance Settings")
		except frappe.DoesNotExistError:
			doc = frappe.new_doc("Instance Settings")
			doc.name = "Instance Settings"
			doc.settings_title = "Default Instance"
			doc.ess_user_limit = 100
			doc.core_user_limit = 50
			doc.database_limit_gb = 10.0
			doc.expiry_date = date(2027, 12, 31)
			doc.insert(ignore_permissions=True)
			return doc

	def is_expired(self):
		"""Check if instance is expired"""
		if not self.expiry_date:
			return False
		return date.today() > self.expiry_date

	def get_status(self):
		"""Get instance status information"""
		return {
			"expired": self.is_expired(),
			"days_remaining": self.get_days_remaining(),
			"ess_users": self.get_ess_user_count(),
			"core_users": self.get_core_user_count(),
			"ess_limit": self.ess_user_limit,
			"core_limit": self.core_user_limit,
			"database_limit_gb": self.database_limit_gb,
			"expiry_date": str(self.expiry_date)
		}


@frappe.whitelist()
def get_instance_status():
	"""API endpoint to get instance status"""
	settings = InstanceSettings.get_instance_settings()
	return settings.get_status()


@frappe.whitelist()
def check_user_limit(user_type="System User"):
	"""Check if user limit is reached"""
	settings = InstanceSettings.get_instance_settings()
	
	if user_type == "System User" or user_type == "core":
		user_count = settings.get_core_user_count()
		limit = settings.core_user_limit
		user_type_label = "Core"
	else:
		user_count = settings.get_ess_user_count()
		limit = settings.ess_user_limit
		user_type_label = "ESS"
	
	if user_count >= limit:
		frappe.throw(f"{user_type_label} user limit ({limit}) reached!")
	
	return {
		"allowed": True,
		"current_count": user_count,
		"limit": limit
	}


@frappe.whitelist()
def check_expiry():
	"""Check if instance is expired"""
	settings = InstanceSettings.get_instance_settings()
	status = settings.get_status()
	
	if status["expired"]:
		frappe.throw("License has expired!")
	
	return status
