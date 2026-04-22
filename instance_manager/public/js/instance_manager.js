// Instance Manager - Homepage Bar Component
// Shows remaining days until license expiry

frappe.provide("instance_manager");

instance_manager.load_instance_bar = function() {
	// Load instance status and show the bar if needed
	frappe.call({
		method: "instance_manager.doctype.instance_settings.instance_settings.get_instance_status",
		callback: function(r) {
			if (r.message) {
				instance_manager.show_instance_bar(r.message);
			}
		}
	});
};

instance_manager.show_instance_bar = function(status) {
	const days_remaining = status.days_remaining;
	const is_expired = status.expired;
	const expiry_date = status.expiry_date;
	
	let message = "";
	let alert_class = "";
	
	if (is_expired) {
		message = `<strong>⚠️ License Expired!</strong> Your instance license expired on ${expiry_date}. Please contact your administrator.`;
		alert_class = "alert-danger";
	} else if (days_remaining <= 7) {
		message = `<strong>⚠️ License Expiring Soon!</strong> Only <strong>${days_remaining}</strong> day(s) left until expiry on ${expiry_date}. Please renew your license.`;
		alert_class = "alert-warning";
	} else if (days_remaining <= 30) {
		message = `<strong>ℹ️ License Expiry Notice:</strong> <strong>${days_remaining}</strong> days left until expiry on ${expiry_date}.`;
		alert_class = "alert-info";
	} else {
		// Don't show bar if more than 30 days
		return;
	}
	
	// Check if bar already exists
	let existing_bar = document.querySelector(".instance-expiry-bar");
	if (existing_bar) {
		existing_bar.remove();
	}
	
	// Create the bar
	const bar = document.createElement("div");
	bar.className = `alert ${alert_class} instance-expiry-bar`;
	bar.style.cssText = `
		margin: 0;
		padding: 12px 15px;
		border-radius: 4px;
		font-size: 14px;
		position: relative;
		z-index: 1000;
	`;
	bar.innerHTML = message;
	
	// Insert at the top of the main content
	const navbar = document.querySelector(".navbar-fixed-top");
	if (navbar) {
		navbar.parentNode.insertBefore(bar, navbar.nextSibling);
	} else {
		const main_section = document.querySelector(".main-section");
		if (main_section) {
			main_section.parentNode.insertBefore(bar, main_section);
		}
	}
};

// Load instance bar on page load
if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", function() {
		instance_manager.load_instance_bar();
	});
} else {
	instance_manager.load_instance_bar();
}

// Reload the bar periodically (every 5 minutes)
setInterval(function() {
	instance_manager.load_instance_bar();
}, 5 * 60 * 1000);

// Also hook into page changes
$(document).on("page-change", function() {
	instance_manager.load_instance_bar();
});
