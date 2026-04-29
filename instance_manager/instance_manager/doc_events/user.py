# Copyright (c) 2026, Your Organization
# License: MIT

from datetime import date

import frappe

from instance_manager.instance_manager.doctype.instance_settings.instance_settings import (
	InstanceSettings,
)


def before_insert_user(doc, method):
	if not doc.enabled:
		return

	if InstanceSettings.is_excluded_user(doc.name):
		return

	settings = InstanceSettings.get_instance_settings()
	if settings.is_expired():
		frappe.throw("License has expired! Cannot create new users.")

	if doc.user_type == "System User":
		core_count = settings.get_core_user_count()
		if core_count >= settings.core_user_limit:
			frappe.throw(f"Core user limit ({settings.core_user_limit}) reached! Cannot add more core users.")
	elif doc.user_type == "Website User":
		ess_count = settings.get_ess_user_count()
		if ess_count >= settings.ess_user_limit:
			frappe.throw(f"ESS user limit ({settings.ess_user_limit}) reached! Cannot add more ESS users.")


def after_insert_user(doc, method):
	if doc.enabled:
		frappe.logger().info(f"User {doc.email} created with type {doc.user_type}")
