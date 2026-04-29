# Copyright (c) 2026, Your Organization
# License: MIT

import frappe

from instance_manager.instance_manager.doctype.instance_settings.instance_settings import (
	InstanceSettings,
)


def get_instance_summary():
	settings = InstanceSettings.get_instance_settings()
	return settings.get_status()


def check_user_limit_before_create(user_type):
	settings = InstanceSettings.get_instance_settings()

	if settings.is_expired():
		return {"allowed": False, "reason": "License has expired"}

	if user_type == "System User":
		count = settings.get_core_user_count()
		limit = settings.core_user_limit
		type_name = "Core"
	else:
		count = settings.get_ess_user_count()
		limit = settings.ess_user_limit
		type_name = "ESS"

	if count >= limit:
		return {"allowed": False, "reason": f"{type_name} user limit ({limit}) reached"}

	return {"allowed": True, "current": count, "limit": limit}


def get_expiry_warning():
	settings = InstanceSettings.get_instance_settings()
	days_remaining = settings.get_days_remaining()

	if settings.is_expired():
		return {"status": "expired", "message": f"License expired on {settings.expiry_date}"}

	if days_remaining <= 7:
		return {
			"status": "critical",
			"days": days_remaining,
			"message": f"License expires in {days_remaining} day(s)",
		}

	if days_remaining <= 30:
		return {
			"status": "warning",
			"days": days_remaining,
			"message": f"License expires in {days_remaining} day(s)",
		}

	return {"status": "ok", "days": days_remaining}


def validate_instance_active():
	settings = InstanceSettings.get_instance_settings()
	if settings.is_expired():
		frappe.throw("This instance license has expired!")


@frappe.whitelist()
def get_dashboard_status():
	settings = InstanceSettings.get_instance_settings()
	status = settings.get_status()

	return {
		"ess_usage": f"{status['ess_users']}/{status['ess_limit']}",
		"core_usage": f"{status['core_users']}/{status['core_limit']}",
		"days_remaining": status["days_remaining"],
		"expired": status["expired"],
		"expiry_date": status["expiry_date"],
	}
