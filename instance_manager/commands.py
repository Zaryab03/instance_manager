# Copyright (c) 2026, Your Organization
# License: MIT

import click
from frappe.commands import pass_context


@click.command("instance-set-expiry")
@click.argument("expiry_date")
@pass_context
def set_expiry_cmd(context, expiry_date):
	"""Set expiry_date override in site_config.json (format: YYYY-MM-DD).

	Example:
	    bench --site mysite instance-set-expiry 2026-12-31
	"""
	from datetime import datetime

	import frappe
	from frappe.installer import update_site_config

	try:
		datetime.strptime(expiry_date, "%Y-%m-%d")
	except ValueError:
		raise click.BadParameter("Use format YYYY-MM-DD", param_hint="expiry_date")

	for site in context.sites:
		try:
			frappe.init(site=site)
			update_site_config("expiry_date", expiry_date)
			click.echo(f"✓  {site}  →  expiry_date = {expiry_date}")
		finally:
			frappe.destroy()


@click.command("instance-renew")
@click.option("--days", default=365, show_default=True, type=int, help="Days to extend")
@click.option(
	"--from-today",
	is_flag=True,
	help="Start from today instead of the current expiry date",
)
@pass_context
def renew_cmd(context, days, from_today):
	"""Extend instance expiry by N days and write to site_config.json.

	The base date is chosen in order:
	  1. Current expiry_date in site_config.json (unless --from-today)
	  2. Expiry date stored in the Instance Settings record (unless --from-today)
	  3. Today

	Example:
	    bench --site mysite instance-renew --days 365
	    bench --site mysite instance-renew --days 90 --from-today
	"""
	from datetime import date, timedelta

	import frappe
	from frappe.installer import update_site_config
	from frappe.utils import getdate

	for site in context.sites:
		try:
			frappe.init(site=site)
			frappe.connect()

			base_date = date.today()
			source = "today"

			if not from_today:
				config_val = frappe.conf.get("expiry_date")
				if config_val:
					base_date = getdate(config_val)
					source = f"site_config ({config_val})"
				else:
					db_val = frappe.db.get_single_value("Instance Settings", "expiry_date")
					if db_val:
						base_date = getdate(db_val)
						source = f"database ({db_val})"

			new_expiry = base_date + timedelta(days=days)
			new_str = new_expiry.isoformat()
			update_site_config("expiry_date", new_str)
			click.echo(f"✓  {site}  →  expiry_date = {new_str}  (+{days} days from {source})")
		finally:
			frappe.destroy()


@click.command("instance-activate")
@pass_context
def activate_cmd(context):
	"""Bypass all expiry checks: write instance_active=1 to site_config.json.

	Use this for emergency access or while processing a renewal.

	Example:
	    bench --site mysite instance-activate
	"""
	import frappe
	from frappe.installer import update_site_config

	for site in context.sites:
		try:
			frappe.init(site=site)
			update_site_config("instance_active", 1)
			click.echo(f"✓  {site}  →  instance_active = 1  (expiry checks bypassed)")
		finally:
			frappe.destroy()


@click.command("instance-deactivate")
@pass_context
def deactivate_cmd(context):
	"""Re-enable expiry checks: set instance_active=0 in site_config.json.

	Example:
	    bench --site mysite instance-deactivate
	"""
	import frappe
	from frappe.installer import update_site_config

	for site in context.sites:
		try:
			frappe.init(site=site)
			update_site_config("instance_active", 0)
			click.echo(f"✓  {site}  →  instance_active = 0  (expiry checks restored)")
		finally:
			frappe.destroy()


@click.command("instance-status")
@pass_context
def status_cmd(context):
	"""Print current instance status (expiry, user counts, overrides).

	Example:
	    bench --site mysite instance-status
	"""
	import frappe

	for site in context.sites:
		try:
			frappe.init(site=site)
			frappe.connect()

			doc = frappe.get_single("Instance Settings")
			s = doc.get_status()

			config_active = frappe.conf.get("instance_active")
			config_expiry = frappe.conf.get("expiry_date")

			state = (
				"SUSPENDED" if s["suspended"]
				else "GRACE PERIOD" if s["in_grace"]
				else "EXPIRED" if s["expired"]
				else "ACTIVE"
			)

			click.echo(f"\n── Instance Status: {site} ──────────────────────────")
			click.echo(f"  State        : {state}")
			click.echo(f"  Expiry Date  : {s['expiry_date'] or 'not set'}")
			click.echo(f"  Days Left    : {s['days_remaining']}")
			click.echo(f"  Grace Left   : {s['grace_days_remaining']} day(s)")
			click.echo(f"  ESS Users    : {s['ess_users']} / {s['ess_limit']}")
			click.echo(f"  Core Users   : {s['core_users']} / {s['core_limit']}")
			if config_active:
				click.echo(f"  [Override]   : instance_active=1  (expiry checks bypassed)")
			if config_expiry:
				click.echo(f"  [Override]   : expiry_date={config_expiry}  (from site_config)")
			click.echo("")
		except Exception as e:
			click.echo(f"✗  {site}: {e}")
		finally:
			frappe.destroy()


commands = [set_expiry_cmd, renew_cmd, activate_cmd, deactivate_cmd, status_cmd]
