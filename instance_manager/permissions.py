# Copyright (c) 2026, Your Organization
# License: MIT

import frappe


def has_permission(doc=None, ptype=None, user=None):
	user = user or frappe.session.user
	return "System Manager" in frappe.get_roles(user)
