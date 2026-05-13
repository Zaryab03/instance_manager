# Instance Manager

Instance Manager is a Frappe control app designed to manage and restrict system-level configurations such as ESS core behavior, server scripts, client scripts, and database usage. It also provides instance-level expiry control with automated user notifications.

## Features

- **User Limits**: Enforce separate limits for ESS (Website Users) and Core (System Users)
- **Database Limits**: Set database size limits for your instance
- **License Expiry Tracking**: Track when your instance license expires
- **Homepage Bar**: Displays remaining days until expiry directly on the Frappe homepage
- **Automatic Checks**: Validates user creation against limits and expiry status

## Installation

1. Add this app to your bench at `apps/instance_manager`.

2. Install the Python package into the bench virtualenv:
```bash
./env/bin/python -m pip install --force-reinstall --no-build-isolation ./apps/instance_manager
```

3. Install the app on your site:
```bash
bench --site your-site install-app instance_manager
```

4. Migrate the database:
```bash
bench --site your-site migrate
```

5. Build assets and clear cache:
```bash
bench build
bench --site your-site clear-cache
```

For this bench, you can also use the bundled installer:
```bash
./apps/instance_manager/install.sh your-site
```

### Why the extra `pip install` step?

Some older or offline bench environments do not automatically install custom app packages into the bench virtualenv before loading hooks. In that case, Frappe can see `instance_manager` in `sites/apps.txt` but Python still raises:

```python
ModuleNotFoundError: No module named 'instance_manager'
```

Installing the app package into `./env` first avoids that issue.

## Configuration

After installation, create an "Instance Settings" document:

1. Go to Awesome Bar and search for "Instance Settings"
2. Create a new Instance Settings document
3. Configure:
   - **Instance Name**: Name of your instance
   - **ESS User Limit**: Maximum Website Users allowed
   - **Core User Limit**: Maximum System Users allowed
   - **Database Limit (GB)**: Maximum database size
   - **Expiry Date**: When the license expires

## Features

### 1. User Limits (ESS and Core)
- Automatically checks limits before creating new users
- Prevents exceeding configured limits
- Shows current usage vs. limits in settings

### 2. License Expiry
- Set an expiry date for your instance
- System shows warning bar when approaching expiry
- Critical warning when less than 7 days remaining
- Expired instances cannot create new users

### 3. Homepage Bar
- Automatically displays on every Frappe page
- Shows remaining days until expiry
- Color-coded alerts:
  - Red: License expired
  - Orange: Less than 7 days remaining
  - Blue: Less than 30 days remaining
- Updates every 5 minutes

## Support

For issues, feature requests, or contributions, please contact your administrator.


## License

MIT License - See LICENSE file for details


## Bench usefull commands

bench --site mysite instance-status
bench --site mysite instance-set-expiry 2026-12-31
bench --site mysite instance-renew --days 365
bench --site mysite instance-activate       # bypass checks
bench --site mysite instance-deactivate     # restore checks


