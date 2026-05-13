# Copyright (c) 2026, Your Organization
# License: MIT

import frappe


def has_permission(doc=None, ptype=None, user=None):
	# Instance Settings is server-only; no role may open it via the desk.
	return False


def has_server_script_permission(doc=None, ptype=None, user=None):
	"""Block Server Script access unless allow_server_script=1 in site_config.json.

	To enable:  bench --site <name> set-config allow_server_script 1
	To disable: bench --site <name> set-config --delete allow_server_script
	"""
	if frappe.conf.get("allow_server_script"):
		return None  # defer to Frappe's default role-based permissions
	return False


def has_client_script_permission(doc=None, ptype=None, user=None):
	"""Block Client Script access unless allow_client_script=1 in site_config.json.

	To enable:  bench --site <name> set-config allow_client_script 1
	To disable: bench --site <name> set-config --delete allow_client_script
	"""
	if frappe.conf.get("allow_client_script"):
		return None  # defer to Frappe's default role-based permissions
	return False
