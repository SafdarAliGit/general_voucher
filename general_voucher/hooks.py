from . import __version__ as app_version

app_name = "general_voucher"
app_title = "General Voucher"
app_publisher = "Tech Ventures"
app_description = "this is installation app"
app_email = "safdar211@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/general_voucher/css/general_voucher.css"
# app_include_js = "/assets/general_voucher/js/general_voucher.js"

# include js, css files in header of web template
# web_include_css = "/assets/general_voucher/css/general_voucher.css"
# web_include_js = "/assets/general_voucher/js/general_voucher.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "general_voucher/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "general_voucher.utils.jinja_methods",
#	"filters": "general_voucher.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "general_voucher.install.before_install"
# after_install = "general_voucher.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "general_voucher.uninstall.before_uninstall"
# after_uninstall = "general_voucher.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "general_voucher.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Journal Entry": "general_voucher.general_voucher.overrides.journal_entry_overrides.JournalEntryOverrides"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"general_voucher.tasks.all"
#	],
#	"daily": [
#		"general_voucher.tasks.daily"
#	],
#	"hourly": [
#		"general_voucher.tasks.hourly"
#	],
#	"weekly": [
#		"general_voucher.tasks.weekly"
#	],
#	"monthly": [
#		"general_voucher.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "general_voucher.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "general_voucher.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "general_voucher.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["general_voucher.utils.before_request"]
# after_request = ["general_voucher.utils.after_request"]

# Job Events
# ----------
# before_job = ["general_voucher.utils.before_job"]
# after_job = ["general_voucher.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"general_voucher.auth.validate"
# ]
