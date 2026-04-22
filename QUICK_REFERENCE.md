# Instance Manager - Quick Reference

## Installation (One-time)

```bash
cd /home/zaryab/version-15
chmod +x apps/instance_manager/install.sh
./apps/instance_manager/install.sh demo.zq.com
```

Or manually:
```bash
bench --site demo.zq.com install-app instance_manager
bench --site demo.zq.com migrate
bench build
```

## Initial Setup

1. **Search** for "Instance Settings" in Awesome Bar
2. **Click** "New"
3. **Fill in** these fields:
   - Instance Name: `Your Instance Name`
   - ESS User Limit: `100` (Website Users)
   - Core User Limit: `50` (System Users)
   - Database Limit (GB): `10`
   - Expiry Date: `YYYY-MM-DD`
4. **Save**

## Check Current Status

### Via Frappe Desk
- Go to "Instance Settings" doctype
- View current usage stats

### Via API (JavaScript)
```javascript
frappe.call({
    method: "instance_manager.doctype.instance_settings.instance_settings.get_instance_status",
    callback: (r) => console.log(r.message)
});
```

### Via API (Browser/curl)
```
GET /api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status
```

### Via Python
```python
from instance_manager.doctype.instance_settings.instance_settings import InstanceSettings
settings = InstanceSettings.get_instance_settings()
print(settings.get_status())
```

## Common Tasks

### Increase ESS User Limit
1. Go to Instance Settings
2. Change "ESS User Limit" value
3. Save
4. Done!

### Increase Core User Limit
1. Go to Instance Settings
2. Change "Core User Limit" value
3. Save
4. Done!

### Extend Expiry Date
1. Go to Instance Settings
2. Change "Expiry Date" to future date
3. Save
4. Done!

### Check User Counts
```javascript
// In browser console or custom app
frappe.call({
    method: "instance_manager.doctype.instance_settings.instance_settings.check_user_limit",
    args: { user_type: "System User" },
    callback: (r) => console.log(r.message)
});
```

## Homepage Bar Behavior

| Days Remaining | Bar Display | Color |
|---|---|---|
| > 30 | Hidden | - |
| 8-30 | "License expires in X days" | Blue |
| 1-7 | "WARNING: Only X days left!" | Orange |
| 0 | "License Expired!" | Red |

## Troubleshooting

### Homepage bar not showing
```bash
bench --site demo.zq.com clear-cache
bench build
```

### User creation limit not enforced
1. Check Instance Settings exists and is saved
2. Clear cache: `bench --site demo.zq.com clear-cache`
3. Verify user_type is set correctly on user

### Data not updating
- Refresh page
- Wait for 5-minute auto-refresh
- Clear browser cache (Ctrl+Shift+Delete)

## API Response Examples

### Get Instance Status
```json
{
  "expired": false,
  "days_remaining": 45,
  "ess_users": 25,
  "core_users": 10,
  "ess_limit": 100,
  "core_limit": 50,
  "database_limit_gb": 10.0,
  "expiry_date": "2026-06-10"
}
```

### Check User Limit
```json
{
  "allowed": true,
  "current_count": 10,
  "limit": 50
}
```

## File Locations

| File | Purpose |
|---|---|
| `hooks.py` | App configuration |
| `instance_manager.py` | Core logic & APIs |
| `user.py` | User creation hooks |
| `instance_utils.py` | Utility functions |
| `instance_manager.js` | Homepage bar UI |

## Support

- **Docs**: See README.md, SETUP_GUIDE.md, COMPLETE_SUMMARY.md
- **Logs**: `bench --site demo.zq.com show-log`
- **Issue**: Check Instance Settings document exists and is saved

## Key Facts

- ✅ Automatically validates on user creation
- ✅ Works for all users (including admins)
- ✅ Homepage bar auto-refreshes every 5 minutes
- ✅ Expiry enforcement is server-side
- ✅ Only System Managers can edit settings
- ✅ Can be customized per your needs

---

**Version:** 1.0.0  
**License:** MIT  
**Created:** April 22, 2026
