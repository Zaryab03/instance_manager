# Copyright (c) 2026, Your Organization
# License: MIT

from datetime import date, timedelta

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class InstanceSettings(Document):
	"""Instance Settings DocType for managing instance limits and expiry."""

	def validate(self):
		if self.ess_user_limit < 0:
			frappe.throw("ESS User Limit cannot be negative")

		if self.core_user_limit < 0:
			frappe.throw("Core User Limit cannot be negative")

		if self.database_limit_gb <= 0:
			frappe.throw("Database Limit must be greater than 0")

		if (self.grace_period_days or 0) < 0:
			frappe.throw("Grace Period cannot be negative")

	def on_update(self):
		self.update_status_info()

	def update_status_info(self):
		days_left = self.get_days_remaining()
		ess_count = self.get_ess_user_count()
		core_count = self.get_core_user_count()
		grace_left = self.get_grace_days_remaining()
		suspended = self.is_suspended()
		in_grace = self.is_in_grace()

		config_active = frappe.conf.get("instance_active")
		config_expiry = frappe.conf.get("expiry_date")

		if suspended:
			state_html = f'<span style="color:#c0392b;font-weight:600;">⛔ Suspended ({self.get_days_since_expiry()} days ago)</span>'
		elif in_grace:
			state_html = f'<span style="color:#e67e22;font-weight:600;">⚠ Grace Period – {grace_left} day(s) remaining</span>'
		elif self.is_expired():
			state_html = '<span style="color:#c0392b;font-weight:600;">Expired</span>'
		else:
			state_html = f'<span style="color:#27ae60;font-weight:600;">Active – {days_left} day(s) remaining</span>'

		override_html = ""
		if config_active:
			override_html = '<p style="color:#8e44ad;font-size:12px;">⚙ Override: instance_active=1 set in site_config.json</p>'
		elif config_expiry:
			override_html = f'<p style="color:#8e44ad;font-size:12px;">⚙ Override: expiry_date="{config_expiry}" set in site_config.json</p>'

		self.status_info = f"""
		<div class="instance-status-info">
			<p><strong>Status:</strong> {state_html}</p>
			<p><strong>ESS Users:</strong> {ess_count} / {self.ess_user_limit}</p>
			<p><strong>Core Users:</strong> {core_count} / {self.core_user_limit}</p>
			{override_html}
		</div>
		"""

	# ── Date helpers ──────────────────────────────────────────────────────────

	def get_expiry_date(self):
		# site_config.json override: bench --site <name> set-config expiry_date "YYYY-MM-DD"
		config_expiry = frappe.conf.get("expiry_date")
		if config_expiry:
			return getdate(config_expiry)
		return getdate(self.expiry_date) if self.expiry_date else None

	def get_grace_end_date(self):
		expiry_date = self.get_expiry_date()
		if not expiry_date:
			return None
		grace_days = self.grace_period_days if self.grace_period_days is not None else 30
		return expiry_date + timedelta(days=grace_days)

	# ── State checks ──────────────────────────────────────────────────────────

	def is_expired(self):
		# site_config.json override: bench --site <name> set-config instance_active 1
		if frappe.conf.get("instance_active"):
			return False
		expiry_date = self.get_expiry_date()
		if not expiry_date:
			return False
		return date.today() > expiry_date

	def is_in_grace(self):
		if frappe.conf.get("instance_active"):
			return False
		expiry_date = self.get_expiry_date()
		if not expiry_date:
			return False
		today = date.today()
		grace_end = self.get_grace_end_date()
		return expiry_date < today <= grace_end

	def is_suspended(self):
		# site_config.json override: bench --site <name> set-config instance_active 1
		if frappe.conf.get("instance_active"):
			return False
		grace_end = self.get_grace_end_date()
		if not grace_end:
			return False
		return date.today() > grace_end

	# ── Day counters ──────────────────────────────────────────────────────────

	def get_days_remaining(self):
		expiry_date = self.get_expiry_date()
		if not expiry_date:
			return -1
		return max((expiry_date - date.today()).days, 0)

	def get_grace_days_remaining(self):
		grace_end = self.get_grace_end_date()
		if not grace_end:
			return 0
		return max((grace_end - date.today()).days, 0)

	def get_days_since_expiry(self):
		expiry_date = self.get_expiry_date()
		if not expiry_date:
			return 0
		return max((date.today() - expiry_date).days, 0)

	# ── User counts ───────────────────────────────────────────────────────────

	_SYSTEM_ACCOUNTS = ["Administrator", "Guest"]
	_EXCLUDED_DOMAINS = ["@abc.com"]

	@classmethod
	def is_excluded_user(cls, email):
		if not email:
			return False
		if email in cls._SYSTEM_ACCOUNTS:
			return True
		return any(email.lower().endswith(domain.lower()) for domain in cls._EXCLUDED_DOMAINS)

	def get_ess_user_count(self):
		filters = [
			["enabled", "=", 1],
			["user_type", "=", "Website User"],
			["name", "not in", self._SYSTEM_ACCOUNTS],
		]
		for domain in self._EXCLUDED_DOMAINS:
			filters.append(["name", "not like", f"%{domain}"])
		return frappe.db.count("User", filters=filters)

	def get_core_user_count(self):
		filters = [
			["enabled", "=", 1],
			["user_type", "=", "System User"],
			["name", "not in", self._SYSTEM_ACCOUNTS],
		]
		for domain in self._EXCLUDED_DOMAINS:
			filters.append(["name", "not like", f"%{domain}"])
		return frappe.db.count("User", filters=filters)

	# ── Public API ────────────────────────────────────────────────────────────

	@staticmethod
	def get_instance_settings():
		return frappe.get_single("Instance Settings")

	def get_status(self):
		expiry_date = self.get_expiry_date()
		suspended = self.is_suspended()
		in_grace = self.is_in_grace()
		expired = self.is_expired()

		return {
			"expired": expired,
			"suspended": suspended,
			"in_grace": in_grace,
			"days_remaining": self.get_days_remaining(),
			"grace_days_remaining": self.get_grace_days_remaining(),
			"days_since_expiry": self.get_days_since_expiry(),
			"grace_period_days": self.grace_period_days if self.grace_period_days is not None else 30,
			"ess_users": self.get_ess_user_count(),
			"core_users": self.get_core_user_count(),
			"ess_limit": self.ess_user_limit,
			"core_limit": self.core_user_limit,
			"database_limit_gb": self.database_limit_gb,
			"expiry_date": expiry_date.isoformat() if expiry_date else None,
		}


@frappe.whitelist()
def get_instance_status():
	try:
		settings = InstanceSettings.get_instance_settings()
		return settings.get_status()
	except Exception:
		return None


@frappe.whitelist()
def check_user_limit(user_type="System User"):
	settings = InstanceSettings.get_instance_settings()

	if user_type in ("System User", "core"):
		user_count = settings.get_core_user_count()
		limit = settings.core_user_limit
		user_type_label = "Core"
	else:
		user_count = settings.get_ess_user_count()
		limit = settings.ess_user_limit
		user_type_label = "ESS"

	if user_count >= limit:
		frappe.throw(f"{user_type_label} user limit ({limit}) reached!")

	return {"allowed": True, "current_count": user_count, "limit": limit}


@frappe.whitelist()
def check_expiry():
	settings = InstanceSettings.get_instance_settings()
	status = settings.get_status()

	if status["suspended"]:
		frappe.throw("Instance has been suspended. Please contact your administrator.")

	return status


@frappe.whitelist()
def check_new_user_allowed():
	settings = InstanceSettings.get_instance_settings()

	core_count = settings.get_core_user_count()
	ess_count = settings.get_ess_user_count()
	core_limit = settings.core_user_limit
	ess_limit = settings.ess_user_limit

	core_exceeded = core_count >= core_limit
	ess_exceeded = ess_count >= ess_limit

	if core_exceeded and ess_exceeded:
		return {
			"allowed": False,
			"reason": (
				f"All user limits have been reached.<br><br>"
				f"Core Users: {core_count} / {core_limit}<br>"
				f"ESS Users: {ess_count} / {ess_limit}"
			),
		}

	return {
		"allowed": True,
		"core_count": core_count,
		"core_limit": core_limit,
		"ess_count": ess_count,
		"ess_limit": ess_limit,
	}


