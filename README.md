# Instance Manager

Instance Manager is a Frappe control app designed to manage and restrict system-level configurations such as ESS core behavior, server scripts, client scripts, and database usage. It also provides instance-level expiry control with automated user notifications.

## Features

- **User Limits**: Enforce separate limits for ESS (Website Users) and Core (System Users)
- **Database Limits**: Set database size limits for your instance
- **License Expiry Tracking**: Track when your instance license expires
- **Homepage Bar**: Displays remaining days until expiry directly on the Frappe homepage
- **Automatic Checks**: Validates user creation against limits and expiry status

## Support

For issues, feature requests, or contributions, please contact your administrator.


## License

MIT License - See LICENSE file for details


## Bench usefull commands

- bench --site mysite instance-status
- bench --site mysite instance-set-expiry 2026-12-31
- bench --site mysite instance-renew --days 365
- bench --site mysite instance-activate       # bypass checks
- bench --site mysite instance-deactivate     # restore checks


