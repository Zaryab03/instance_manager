# Instance Manager - Setup and Usage Guide

## Quick Start

### 1. Installation Steps

```bash
# Navigate to your Frappe bench directory
cd /home/zaryab/version-15

# Get the app (already exists at apps/instance_manager)
# Or clone if in a separate repo:
# bench get-app instance-manager https://github.com/your-org/instance-manager

# Install the Python package into the bench virtualenv first
./env/bin/python -m pip install --force-reinstall --no-build-isolation ./apps/instance_manager

# Install on your site
bench --site demo.zq.com install-app instance_manager

# Migrate to create DocType
bench --site demo.zq.com migrate

# Build assets
bench build

# Clear cache
bench --site demo.zq.com clear-cache
```

### Why this step order matters

In some fresh, offline, or older bench environments, `bench --site ... install-app` can run before the custom app is importable from the bench virtualenv. When that happens, hooks fail to load with `ModuleNotFoundError: No module named 'instance_manager'`.

Installing `apps/instance_manager` into `./env` first makes the Python package available before Frappe evaluates hooks and DocType imports.

### 2. Initial Configuration

After installation, configure Instance Settings:

1. **Go to Instance Settings DocType**
   - Navigate to Awesome Bar (Ctrl+K or Cmd+K)
   - Search for "Instance Settings"
   - Click on "Instance Settings"

2. **Create a New Instance Settings Document**
   - Click "New" button
   - Fill in the following fields:

   | Field | Value | Example |
   |-------|-------|---------|
   | Instance Name | Your instance identifier | "Production Instance" |
   | ESS User Limit | Max Website Users | 100 |
   | Core User Limit | Max System Users | 50 |
   | Database Limit (GB) | Max DB size | 10.0 |
   | Expiry Date | License expiry date | 2026-12-31 |

3. **Save the document**

## Features in Detail

### A. User Limits

The app automatically validates user creation against configured limits.

#### ESS Users (Website Users)
- Default limit: 100
- Used for non-internal users
- Includes customers, portal users, etc.
- Limit checked before user creation

#### Core Users (System Users)
- Default limit: 50
- Used for internal staff
- Includes employees, administrators, etc.
- Limit checked before user creation

**What happens when limit is reached?**
- New user creation is rejected
- User sees error message: "Core user limit (50) reached!"
- Existing users can still be enabled

#### How to increase limits
1. Go to Instance Settings
2. Edit ESS User Limit or Core User Limit
3. Save changes
4. New users can now be created

### B. Database Limits

You can set a maximum database size limit (currently for reference/monitoring).

- Default: 10.0 GB
- Displayed in Instance Settings
- Can be used for custom validation scripts

### C. License Expiry

Track when your instance license expires.

**What happens on expiry?**
- New users cannot be created
- System shows "License Expired" message
- Existing users can still log in
- Homepage bar displays critical alert

**What happens before expiry?**
- 30 days before: Info bar displayed
- 7 days before: Warning bar displayed (orange)
- At expiry: Critical alert bar displayed (red)

### D. Homepage Bar

Automatically displayed on every Frappe page.

**Display Logic:**
- Hidden if more than 30 days remaining
- Info (blue) bar: 8-30 days remaining
- Warning (orange) bar: 1-7 days remaining
- Critical (red) bar: Expired

**Format:**
```
ℹ️ License Expiry Notice: 15 days left until expiry on 2026-06-15.
```

**Location:** Appears right below the navbar on every page

## API Reference

### 1. Get Instance Status

**Endpoint:** `/api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status`

**Method:** GET (or POST)

**No Parameters**

**Response:**
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

**Usage Example:**
```javascript
frappe.call({
    method: "instance_manager.doctype.instance_settings.instance_settings.get_instance_status",
    callback: function(r) {
        console.log("Days remaining:", r.message.days_remaining);
    }
});
```

### 2. Check User Limit

**Endpoint:** `/api/method/instance_manager.doctype.instance_settings.instance_settings.check_user_limit`

**Method:** GET

**Parameters:**
- `user_type` (optional): "System User" or "Website User" (default: "System User")

**Response:**
```json
{
  "allowed": true,
  "current_count": 12,
  "limit": 50
}
```

**Or on limit reached:**
```json
{
  "exception": "Core user limit (50) reached!"
}
```

### 3. Check Expiry

**Endpoint:** `/api/method/instance_manager.doctype.instance_settings.instance_settings.check_expiry`

**Method:** GET

**Response:** Same as get_instance_status

### 4. Get Dashboard Status

**Endpoint:** `/api/method/instance_manager.utils.instance_utils.get_dashboard_status`

**Response:**
```json
{
  "ess_usage": "45/100",
  "core_usage": "12/50",
  "days_remaining": 180,
  "expired": false,
  "expiry_date": "2026-12-31"
}
```

## Python API

### Using in Custom Scripts

```python
from instance_manager.doctype.instance_settings.instance_settings import InstanceSettings
from instance_manager.utils.instance_utils import check_user_limit_before_create

# Get instance settings
settings = InstanceSettings.get_instance_settings()

# Check if expired
if settings.is_expired():
    print("License expired!")

# Get days remaining
days = settings.get_days_remaining()
print(f"Days remaining: {days}")

# Get user counts
ess_count = settings.get_ess_user_count()
core_count = settings.get_core_user_count()
print(f"ESS: {ess_count}, Core: {core_count}")

# Check if can create user
can_create = check_user_limit_before_create("System User")
```

## File Structure

```
instance_manager/
├── hooks.py                          # App hooks and configuration
├── package.json                      # Node.js dependencies
├── pyproject.toml                    # Python project config
├── README.md                         # Documentation
├── LICENSE                           # MIT License
├── SETUP_GUIDE.md                   # This file
├── instance_manager/
│   ├── __init__.py                  # Package init
│   ├── doctype/
│   │   ├── __init__.py
│   │   └── instance_settings/
│   │       ├── __init__.py
│   │       ├── instance_settings.json    # DocType definition
│   │       └── instance_settings.py      # Python class with methods
│   ├── doc_events/
│   │   ├── __init__.py
│   │   └── user.py                  # User creation validations
│   ├── utils/
│   │   ├── __init__.py
│   │   └── instance_utils.py        # Utility functions
│   └── public/
│       └── js/
│           └── instance_manager.js   # Homepage bar component
```

## Common Tasks

### Increase User Limits

1. Go to Instance Settings
2. Edit the ESS User Limit or Core User Limit
3. Click Save
4. Done!

### Extend License Expiry

1. Go to Instance Settings
2. Update the Expiry Date field
3. Click Save
4. Homepage bar will update

### Monitor Current Usage

```bash
# Using bench console
bench --site demo.zq.com console

# In Python console:
from instance_manager.doctype.instance_settings.instance_settings import InstanceSettings
settings = InstanceSettings.get_instance_settings()
print(settings.get_status())
```

### Check Limits via API

```bash
# Using curl
curl "http://your-domain/api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status"

# Or from browser console (if logged in)
frappe.call({
    method: "instance_manager.doctype.instance_settings.instance_settings.get_instance_status",
    callback: (r) => console.log(r.message)
});
```

## Troubleshooting

### 1. Homepage Bar Not Showing

**Possible causes:**
- App not installed on site
- Cache not cleared
- More than 30 days remaining

**Solution:**
```bash
bench --site demo.zq.com clear-cache
bench build
```

### 2. User Creation Still Allowed After Limit Reached

**Possible causes:**
- User created by database admin (bypasses validation)
- Old user document cached

**Solution:**
- Clear browser cache
- Check Instance Settings document exists
- Verify user_type field is set correctly

### 3. Expiry Date Not Updating

**Solution:**
- Clear browser cache
- Refresh Instance Settings page
- Wait for next 5-minute refresh cycle

## Security Notes

- Only System Managers can view/edit Instance Settings
- User creation hooks run even for admin users (enforces limits globally)
- Expiry date checks are server-side (cannot be bypassed from frontend)

## Support

For issues or questions:
1. Check logs: `bench --site demo.zq.com show-log`
2. Check Instance Settings document exists and is saved
3. Clear cache and rebuild: `bench --site demo.zq.com clear-cache && bench build`

## Next Steps

- Customize homepage bar styling in `instance_manager/public/js/instance_manager.js`
- Add database size monitoring (currently just a field)
- Add email notifications before expiry
- Add audit logging for user creation attempts
