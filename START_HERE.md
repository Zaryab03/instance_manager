✨ **INSTANCE MANAGER - CUSTOM FRAPPE APP** ✨

Your custom app has been created! Here's what you have:

📁 **Location:** /home/zaryab/version-15/apps/instance_manager

🎯 **Features:**
✓ ESS User Limit (Website Users)
✓ Core User Limit (System Users)  
✓ Database Size Limit
✓ License Expiry Date
✓ Automatic User Creation Validation
✓ Homepage Countdown Bar
✓ Full REST API

─────────────────────────────────────────────────────────────

🚀 QUICK START (3 steps):

1️⃣ INSTALL
   cd /home/zaryab/version-15
   chmod +x apps/instance_manager/install.sh
   ./apps/instance_manager/install.sh demo.zq.com

   Manual equivalent:
   ./env/bin/python -m pip install --force-reinstall --no-build-isolation ./apps/instance_manager
   bench --site demo.zq.com install-app instance_manager
   bench --site demo.zq.com migrate
   bench build
   bench --site demo.zq.com clear-cache

2️⃣ CONFIGURE
   • Open Frappe
   • Search "Instance Settings" in Awesome Bar
   • Click "New"
   • Fill in your limits and expiry date
   • Save

3️⃣ USE
   • Homepage bar appears automatically
   • User creation is validated automatically
   • Check API: /api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status

─────────────────────────────────────────────────────────────

📖 DOCUMENTATION:

For quick commands:
→ Read: QUICK_REFERENCE.md

For detailed setup:
→ Read: SETUP_GUIDE.md

For complete overview:
→ Read: COMPLETE_SUMMARY.md

For architecture details:
→ Read: ARCHITECTURE.md

─────────────────────────────────────────────────────────────

📋 WHAT'S INCLUDED:

Core Files:
├── instance_settings.json      DocType definition
├── instance_settings.py        Main logic with APIs
├── user.py                     User creation validation
├── instance_manager.js         Homepage bar UI
├── instance_utils.py           Utility functions
└── hooks.py                    App configuration

Documentation:
├── README.md                   Quick overview
├── SETUP_GUIDE.md              Detailed guide
├── QUICK_REFERENCE.md          Commands reference
├── COMPLETE_SUMMARY.md         Full summary
└── ARCHITECTURE.md             System design

─────────────────────────────────────────────────────────────

⚙️ CONFIGURATION EXAMPLE:

When you create Instance Settings, set:
  Instance Name: "Production"
  ESS User Limit: 100
  Core User Limit: 50
  Database Limit: 10 GB
  Expiry Date: 2026-12-31

─────────────────────────────────────────────────────────────

🔧 HOMEPAGE BAR BEHAVIOR:

More than 30 days left:
  → Bar is HIDDEN

8-30 days left:
  → Shows BLUE info bar

1-7 days left:
  → Shows ORANGE warning bar

License expired:
  → Shows RED critical alert

─────────────────────────────────────────────────────────────

📊 API ENDPOINTS:

1. Get Status (JSON):
   /api/method/instance_manager.doctype.instance_settings.instance_settings.get_instance_status

2. Check User Limit:
   /api/method/instance_manager.doctype.instance_settings.instance_settings.check_user_limit?user_type=System User

3. Check Expiry:
   /api/method/instance_manager.doctype.instance_settings.instance_settings.check_expiry

4. Dashboard Status:
   /api/method/instance_manager.utils.instance_utils.get_dashboard_status

─────────────────────────────────────────────────────────────

💡 KEY FACTS:

✓ Automatically validates on user creation
✓ Works for all users (including admins)
✓ Server-side enforcement (cannot be bypassed)
✓ Only System Managers can edit settings
✓ Homepage bar auto-refreshes every 5 minutes
✓ REST API available for external integrations
✓ Fully customizable

─────────────────────────────────────────────────────────────

⚠️ IMPORTANT:

• The app requires Frappe framework (already installed)
• Works with Frappe v14+
• Database must have tabUser table
• Only one Instance Settings document needed
• Fresh or offline benches should install the Python package into `./env` before `bench install-app`

─────────────────────────────────────────────────────────────

🆘 TROUBLESHOOTING:

If homepage bar doesn't show:
  bench --site demo.zq.com clear-cache
  bench build

If user creation still allowed:
  1. Check Instance Settings exists
  2. Clear cache
  3. Reload page

If API returns error:
  bench --site demo.zq.com show-log

─────────────────────────────────────────────────────────────

📞 NEXT STEPS:

1. Read QUICK_REFERENCE.md for commands
2. Run ./install.sh to install on your site
3. Create Instance Settings from Frappe UI
4. Test by creating a user (will be validated)
5. Check homepage bar
6. Customize as needed

─────────────────────────────────────────────────────────────

🎉 YOU'RE ALL SET!

The app is ready to install and use.
Start with: QUICK_REFERENCE.md or SETUP_GUIDE.md

Questions? Check ARCHITECTURE.md for system design.

License: MIT
Version: 1.0.0
Created: April 22, 2026

─────────────────────────────────────────────────────────────
