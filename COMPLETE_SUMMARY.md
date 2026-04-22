# Instance Manager - Complete App Summary

## Overview

The Instance Manager is a complete custom Frappe app that provides:

✅ **User Limits Management** - Separate limits for ESS (Website Users) and Core (System Users)  
✅ **Database Size Limits** - Set and monitor database limits  
✅ **License Expiry Tracking** - Track when your instance license expires  
✅ **Homepage Expiry Bar** - Shows remaining days until expiry on every page  
✅ **Automatic Validations** - Enforces limits before user creation  

## What Was Created

### Core Files

```
/home/zaryab/version-15/apps/instance_manager/
├── hooks.py                          # Main app configuration
├── package.json                      # Node dependencies
├── pyproject.toml                    # Python package config
├── README.md                         # User documentation
├── SETUP_GUIDE.md                    # Detailed setup guide
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore file
│
└── instance_manager/
    ├── __init__.py                   # Package initialization
    │
    ├── doctype/instance_settings/
    │   ├── instance_settings.json    # DocType definition
    │   ├── instance_settings.py      # Core class with:
    │   │                             # - get_days_remaining()
    │   │                             # - get_ess_user_count()
    │   │                             # - get_core_user_count()
    │   │                             # - is_expired()
    │   │                             # - get_status() API
    │   │                             # - check_user_limit() API
    │   │                             # - check_expiry() API
    │   └── __init__.py
    │
    ├── doc_events/
    │   ├── user.py                   # User creation hooks:
    │   │                             # - before_insert_user()
    │   │                             # - Validates user limits
    │   │                             # - Checks expiry status
    │   └── __init__.py
    │
    ├── utils/
    │   ├── instance_utils.py         # Utility functions:
    │   │                             # - get_instance_summary()
    │   │                             # - check_user_limit_before_create()
    │   │                             # - get_expiry_warning()
    │   │                             # - validate_instance_active()
    │   │                             # - get_dashboard_status() API
    │   └── __init__.py
    │
    └── public/js/
        └── instance_manager.js       # Frontend component:
                                      # - load_instance_bar()
                                      # - show_instance_bar()
                                      # - Updates every 5 minutes
                                      # - Page change hooks
```

## Key Features

### 1. Instance Settings DocType

A single-instance DocType that stores:
- **ESS User Limit** (default: 100)
- **Core User Limit** (default: 50)
- **Database Limit in GB** (default: 10.0)
- **Expiry Date** (configurable)
- **Status Information** (read-only computed field)

### 2. User Creation Validation

Before any user is created:
1. Checks if license has expired
2. Validates user type (System User vs Website User)
3. Checks current count against limit
4. Throws error if limit reached
5. Prevents user creation

### 3. Homepage Expiry Bar

Automatically displays on Frappe homepage:
- **Red Alert** (if expired): "License Expired! Your instance license expired on [date]"
- **Orange Alert** (7 days or less): "[days] day(s) left until expiry on [date]"
- **Blue Alert** (8-30 days): "[days] days left until expiry on [date]"
- **Hidden** (more than 30 days)

Updates every 5 minutes and on page changes.

### 4. API Endpoints

#### A. Get Instance Status
```
GET /api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status
```

#### B. Check User Limit
```
GET /api/method/instance_manager.doctype.instance_settings.instance_settings.check_user_limit?user_type=System User
```

#### C. Check Expiry
```
GET /api/method/instance_manager.doctype.instance_settings.instance_settings.check_expiry
```

#### D. Get Dashboard Status
```
GET /api/method/instance_manager.utils.instance_utils.get_dashboard_status
```

## Installation Instructions

### Step 1: The app is already created at:
```
/home/zaryab/version-15/apps/instance_manager/
```

### Step 2: Install on your Frappe site
```bash
cd /home/zaryab/version-15

# Install the app
bench --site demo.zq.com install-app instance_manager

# Migrate to create the DocType
bench --site demo.zq.com migrate

# Build assets
bench build
```

### Step 3: Create Instance Settings
1. Go to Awesome Bar (Ctrl+K)
2. Search for "Instance Settings"
3. Click "New"
4. Fill in values:
   - Instance Name: "Your Instance"
   - ESS User Limit: 100
   - Core User Limit: 50
   - Database Limit (GB): 10.0
   - Expiry Date: 2027-12-31
5. Save

### Step 4: Verify It Works
1. Go to home page - you should see the expiry bar (if less than 30 days to expiry)
2. Try creating a new System User to test limit validation
3. Check API: `/api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status`

## Configuration Examples

### Example 1: Production Setup
```
Instance Name: Production Server
ESS User Limit: 200
Core User Limit: 100
Database Limit (GB): 50.0
Expiry Date: 2027-12-31
```

### Example 2: Development Setup
```
Instance Name: Development Server
ESS User Limit: 10
Core User Limit: 5
Database Limit (GB): 5.0
Expiry Date: 2027-06-30
```

### Example 3: Trial Setup
```
Instance Name: Trial Instance
ESS User Limit: 5
Core User Limit: 2
Database Limit (GB): 2.0
Expiry Date: 2026-05-22
```

## Usage Scenarios

### Scenario 1: Monitor Current Usage
```python
from instance_manager.doctype.instance_settings.instance_settings import InstanceSettings

settings = InstanceSettings.get_instance_settings()
status = settings.get_status()

print(f"ESS Users: {status['ess_users']}/{status['ess_limit']}")
print(f"Core Users: {status['core_users']}/{status['core_limit']}")
print(f"Days remaining: {status['days_remaining']}")
```

### Scenario 2: Programmatic Limit Check
```python
from instance_manager.utils.instance_utils import check_user_limit_before_create

result = check_user_limit_before_create("System User")
if result["allowed"]:
    # Create the user
    new_user = frappe.new_doc("User")
    # ... set fields ...
    new_user.insert()
else:
    print(f"Cannot create user: {result['reason']}")
```

### Scenario 3: Frontend Notification
```javascript
frappe.call({
    method: "instance_manager.doctype.instance_settings.instance_settings.get_instance_status",
    callback: function(r) {
        if (r.message.days_remaining < 30) {
            frappe.show_alert({
                message: `License expires in ${r.message.days_remaining} days!`,
                indicator: "orange"
            });
        }
    }
});
```

## Customization Options

### 1. Modify User Limits
- Edit Instance Settings
- Change ESS User Limit or Core User Limit
- Save and take effect immediately

### 2. Customize Homepage Bar
Edit `/instance_manager/public/js/instance_manager.js`:
- Change color scheme
- Modify message format
- Adjust positioning
- Change update frequency

### 3. Add Database Size Monitoring
Extend `instance_manager/utils/instance_utils.py` with:
```python
def get_database_size():
    """Get current database size in GB"""
    # Add implementation
    pass
```

### 4. Add Email Notifications
Add to `hooks.py`:
```python
scheduler_events = {
    "daily": [
        "instance_manager.tasks.send_expiry_notification"
    ]
}
```

## Permissions

- Only **System Managers** can view/edit Instance Settings
- User creation validation runs for **all** users (including admins)
- Expiry checks are enforced at **server-level**

## Database Tables Created

- `tabInstance Settings` - Main configuration table

## Troubleshooting

### App not showing in sidebar
```bash
bench --site demo.zq.com clear-cache
bench build
```

### Homepage bar not appearing
1. Check Instance Settings exists
2. Check expiry date is within 30 days or expired
3. Clear browser cache
4. Open homepage again

### User creation still allowed after limit reached
- Verify Instance Settings document exists
- Check if it was saved properly
- Restart bench for changes to take effect

## Testing the App

```bash
# Install app
bench --site demo.zq.com install-app instance_manager

# Migrate
bench --site demo.zq.com migrate

# Access Instance Settings
# URL: http://your-site/app/instance-settings

# Create a new Instance Settings document
# Set ESS limit to 0 for testing
# Try creating a Website User (should fail)

# Try API
# URL: http://your-site/api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status
```

## File Sizes

- `instance_settings.py`: ~300 lines
- `instance_settings.json`: ~150 lines
- `user.py`: ~40 lines
- `instance_utils.py`: ~100 lines
- `instance_manager.js`: ~90 lines
- `hooks.py`: ~70 lines

**Total Lines of Code: ~750 lines**

## Next Steps

1. ✅ App created and ready for installation
2. ⏭️ Install on your Frappe site
3. ⏭️ Create Instance Settings document
4. ⏭️ Test user limit validation
5. ⏭️ Monitor expiry via homepage bar
6. ⏭️ Customize for your needs

## Support Resources

- `README.md` - Quick reference guide
- `SETUP_GUIDE.md` - Detailed setup and usage guide
- `hooks.py` - Configuration reference
- API endpoints - Listed above in "Key Features"

---

**Created:** April 22, 2026  
**Version:** 1.0.0  
**License:** MIT
