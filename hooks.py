# Copyright (c) 2026, Your Organization
# License: MIT

app_name = "instance_manager"
app_title = "Instance Manager"
app_publisher = "Your Organization"
app_description = "Manage instance limits, user counts, and license expiry"
app_email = "info@example.com"
app_license = "MIT"
app_version = "1.0.0"

# Apps that should be installed before this one
depends_on = ["frappe"]

# Include CSS, JS files in header of desk.html
app_include_css = []
app_include_js = ["/assets/instance_manager/js/instance_manager.js"]

# Include js, css files in web form
web_include_css = []
web_include_js = []

# Include custom scss in every website page
website_context = {}

# Web page routes
# page_routes = {
#   "page-name": "path/to/the/page"
# }

# Modules
# modules = [
#   {
#     "app_name": "instance_manager",
#     "module_name": "Instance Manager"
#   }
# ]

fixtures = [
	{"dt": "Custom DocType", "filters": [["name", "in", []]]},
]

# Included doctypes or custom doctypes
# doctype_js = {
# 	"doctype_name": "path/to/doctype_js"
# }
doctype_js = {}

# Home Pages
# homepage_template = "app_name/templates/home.html"

# Website Generators
# page_length = 500

# Web Form
# webform_list_context = {}

# Hooks
fixtures = []

# Doc Events
doc_events = {
	"User": {
		"before_insert": "instance_manager.doc_events.user.before_insert_user",
		"after_insert": "instance_manager.doc_events.user.after_insert_user"
	}
}

# Scheduled Tasks
# scheduler_events = {
# 	"all": [
# 		"instance_manager.tasks.all"
# 	],
# 	"daily": [
# 		"instance_manager.tasks.daily"
# 	],
# 	"hourly": [
# 		"instance_manager.tasks.hourly"
# 	],
# 	"weekly": [
# 		"instance_manager.tasks.weekly"
# 	],
# 	"monthly": [
# 		"instance_manager.tasks.monthly"
# 	]
# }

# Jinja
# jinja = {
# 	"methods": "instance_manager.utils.get_methods",
# 	"filters": "instance_manager.utils.get_filters"
# }

# Testing
# test_runner = "frappe.test_runner.TestRunner"

# On Document Event
# doc_events = {
# 	"DocType Name":{
# 		"on_update": "instance_manager.module.method",
# 		"on_submit": "instance_manager.module.method",
# 		"before_insert": "instance_manager.module.method"
# 	}
# }

# Permissions
has_permission = {
	"Instance Settings": "instance_manager.permissions.has_permission"
}

# Portal Pages
# has_website_permission = {
# 	"doctype_name": "instance_manager.module.method"
# }

# Translated DocTypes
# get_translated_dict = {
# 	"doctype_name": "instance_manager.module.get_dict"
# }

# API Routes
# @frappe.whitelist functions will be mapped automatically
