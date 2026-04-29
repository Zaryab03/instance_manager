# Copyright (c) 2026, Your Organization
# License: MIT

app_name = "instance_manager"
app_title = "Instance Manager"
app_publisher = "Your Organization"
app_description = "Manage instance limits, user counts, and license expiry"
app_email = "info@example.com"
app_license = "MIT"
app_version = "1.0.0"

depends_on = ["frappe"]

app_include_css = ["/assets/instance_manager/css/instance_manager.css"]
app_include_js = ["/assets/instance_manager/js/instance_manager.js"]

web_include_css = []
web_include_js = []

website_context = {}

doctype_js = {}

fixtures = []

doc_events = {
	"User": {
		"before_insert": "instance_manager.instance_manager.doc_events.user.before_insert_user",
		"after_insert": "instance_manager.instance_manager.doc_events.user.after_insert_user",
	}
}

has_permission = {
	"Instance Settings": "instance_manager.instance_manager.permissions.has_permission",
	"Server Script": "instance_manager.instance_manager.permissions.has_server_script_permission",
	"Client Script": "instance_manager.instance_manager.permissions.has_client_script_permission",
}
