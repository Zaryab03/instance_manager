# Instance Manager

A custom Frappe app for managing instance-level limits and license expiry.

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

## API Endpoints

### Get Instance Status
```
GET /api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status
```

Returns:
```json
{
  "expired": false,
  "days_remaining": 180,
  "ess_users": 45,
  "core_users": 12,
  "ess_limit": 100,
  "core_limit": 50,
  "database_limit_gb": 10.0,
  "expiry_date": "2026-12-31"
}
```

### Check User Limit
```
GET /api/method/instance_manager.doctype.instance_settings.instance_settings.check_user_limit
Parameters: user_type=System User|Website User
```

### Check Expiry
```
GET /api/method/instance_manager.doctype.instance_settings.instance_settings.check_expiry
```

## Usage Examples

### Check limits before creating a user
```python
from instance_manager.doctype.instance_settings.instance_settings import check_user_limit

result = check_user_limit("System User")
if result["allowed"]:
    # Create user
    pass
else:
    print(f"Cannot create user: {result['reason']}")
```

### Get current status
```python
from instance_manager.utils.instance_utils import get_instance_summary

summary = get_instance_summary()
print(f"Days remaining: {summary['days_remaining']}")
```

## Permissions

By default, only System Managers can view and edit Instance Settings.

## Support

For issues, feature requests, or contributions, please contact your administrator.

## License

MIT License - See LICENSE file for details
