# Instance Manager - Architecture & Overview

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frappe Dashboard                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 🟠 Homepage Expiry Bar (instance_manager.js)         │  │
│  │ "⚠️ License expires in 5 days on 2026-05-27"        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  All Frappe Pages / Forms / Lists                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend (Python / Server-Side)                 │
│                                                              │
│  ┌─ Instance Settings (DocType) ─────────────────────────┐ │
│  │ • ESS User Limit: 100                                │ │
│  │ • Core User Limit: 50                                │ │
│  │ • Database Limit: 10 GB                              │ │
│  │ • Expiry Date: 2026-12-31                            │ │
│  └────────────────────────────────────────────────────┘ │
│                            ↓                               │
│  ┌─ User Creation Hook (doc_events/user.py) ──────────┐ │
│  │ Before User Insert:                                │ │
│  │ 1. Check if expired → Throw error                 │ │
│  │ 2. Check user type (ESS/Core)                     │ │
│  │ 3. Count existing users of that type              │ │
│  │ 4. Compare against limit → Allow/Reject           │ │
│  └────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─ API Endpoints ───────────────────────────────────────┐ │
│  │ • get_instance_status()                            │ │
│  │ • check_user_limit()                               │ │
│  │ • check_expiry()                                   │ │
│  │ • get_dashboard_status()                           │ │
│  └────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─ Utility Functions (utils/instance_utils.py) ──────┐ │
│  │ • get_instance_summary()                           │ │
│  │ • check_user_limit_before_create()                 │ │
│  │ • get_expiry_warning()                             │ │
│  │ • validate_instance_active()                       │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Database (MySQL/MariaDB)                        │
│                                                              │
│  tabInstance_Settings                                      │
│  ├── name: "Instance Settings"                            │
│  ├── ess_user_limit: 100                                  │
│  ├── core_user_limit: 50                                  │
│  ├── database_limit_gb: 10.0                              │
│  └── expiry_date: 2026-12-31                              │
│                                                              │
│  tabUser (existing)                                        │
│  ├── user_type: "System User"                             │
│  ├── enabled: 1                                           │
│  └── ... [existing user fields]                           │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Component Breakdown

### 1. Frontend Component
**File:** `instance_manager/public/js/instance_manager.js`
- Loads on page initialization
- Fetches instance status via API
- Renders colored alert bar
- Auto-refreshes every 5 minutes
- Hooks into page navigation

### 2. Core DocType
**File:** `instance_manager/doctype/instance_settings/instance_settings.json`
**Python Class:** `instance_manager/doctype/instance_settings/instance_settings.py`

Methods:
- `validate()` - Validates configuration
- `get_days_remaining()` - Calculates days to expiry
- `get_ess_user_count()` - Count active ESS users
- `get_core_user_count()` - Count active Core users
- `is_expired()` - Check if license expired
- `get_status()` - Return comprehensive status
- `get_instance_settings()` - Singleton getter
- Static APIs for external calls

### 3. User Validation Hook
**File:** `instance_manager/doc_events/user.py`

Runs before any user is inserted:
1. Checks if instance expired
2. Identifies user type
3. Counts existing users of that type
4. Throws error if limit reached

### 4. Utility Functions
**File:** `instance_manager/utils/instance_utils.py`

Helper functions for:
- Getting instance summary
- Checking limits programmatically
- Getting expiry warnings
- Dashboard status

### 5. App Configuration
**File:** `hooks.py`

Registers:
- App metadata
- Doc event hooks
- JavaScript includes
- Permissions

## 📋 Data Flow

### User Creation Flow
```
User clicks "New" → Creates User Form
        ↓
User fills details and clicks Save
        ↓
Server receives insert request
        ↓
doc_events/user.py::before_insert_user() triggered
        ↓
Check: Is instance expired?
  YES → Throw "License expired!"
  NO → Continue
        ↓
Check: User type (System vs Website)?
  System User → Get core user count
  Website User → Get ESS user count
        ↓
Compare count vs limit
  Count < Limit → Allow insert
  Count >= Limit → Throw "Limit reached!"
        ↓
User created (or creation rejected)
```

### Homepage Bar Display Flow
```
Page loads in browser
        ↓
instance_manager.js loads
        ↓
Call: get_instance_status() API
        ↓
Server returns status with days_remaining
        ↓
JavaScript checks days_remaining
  > 30 days → Do nothing (hide bar)
  8-30 days → Show blue info bar
  1-7 days → Show orange warning bar
  <= 0 days → Show red critical bar
        ↓
Render alert bar below navbar
        ↓
Set timer for refresh in 5 minutes
```

## 🔐 Security Measures

1. **Server-Side Validation**
   - All limit checks happen on server
   - Cannot be bypassed from frontend
   - Applies to all users including admins

2. **Permission Control**
   - Only System Managers can edit Instance Settings
   - DocType has explicit permissions

3. **Expiry Enforcement**
   - Checked at user creation time
   - Prevents new users if expired
   - Cannot be bypassed

## 📊 Usage Statistics

### Files Created: 19
- Python files: 6
- JSON files: 1
- JavaScript files: 1
- Configuration files: 4
- Documentation: 5
- Other: 2

### Total Lines of Code: ~750
- Python: ~450 lines
- JavaScript: ~90 lines
- JSON: ~150 lines
- Configuration: ~60 lines

### API Endpoints: 4
- get_instance_status
- check_user_limit
- check_expiry
- get_dashboard_status

## 🚀 Installation Steps

```bash
# 1. Navigate to bench
cd /home/zaryab/version-15

# 2. Make install script executable
chmod +x apps/instance_manager/install.sh

# 3. Run installation
./apps/instance_manager/install.sh demo.zq.com

# 4. Create Instance Settings from Frappe UI
# Go to Awesome Bar → Search "Instance Settings" → New
```

## ✅ What You Get

✅ **User Limits**
- Separate ESS and Core user limits
- Automatic enforcement
- Real-time counting

✅ **License Expiry**
- Track expiry date
- Prevent user creation on expiry
- Visual countdown

✅ **Homepage Bar**
- Shows remaining days
- Color-coded alerts
- Auto-updating

✅ **Full API**
- Get status
- Check limits
- Validate expiry
- Dashboard info

✅ **Admin Dashboard**
- View current usage
- Edit limits anytime
- Monitor status

## 📈 Next Steps

1. Install the app
2. Create Instance Settings document
3. Configure your limits and expiry
4. See homepage bar in action
5. Try creating users (limit validation)
6. Customize as needed

## 🎨 Customization Examples

### Change homepage bar color
Edit `instance_manager/public/js/instance_manager.js`:
```javascript
alert_class = "alert-danger"; // Change color
```

### Customize alert message
Edit the message string in `show_instance_bar()` function

### Add database size monitoring
Extend `instance_utils.py` with database size check

### Send email on expiry
Add scheduled task to `hooks.py`

## 📚 Documentation Files

1. **README.md** - Overview and quick start
2. **SETUP_GUIDE.md** - Detailed setup and usage guide
3. **COMPLETE_SUMMARY.md** - Full app summary
4. **QUICK_REFERENCE.md** - Command reference
5. **This file** - Architecture overview

## 📞 Support

- Check logs: `bench --site demo.zq.com show-log`
- Clear cache: `bench --site demo.zq.com clear-cache`
- Rebuild: `bench build`
- Reinstall: `./install.sh demo.zq.com`

---

**Ready to use!** Start with QUICK_REFERENCE.md for quick commands or SETUP_GUIDE.md for detailed guide.
