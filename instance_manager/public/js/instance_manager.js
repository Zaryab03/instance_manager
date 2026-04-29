frappe.provide("instance_manager");

instance_manager.load_instance_bar = function () {
	frappe.call({
		method: "instance_manager.instance_manager.doctype.instance_settings.instance_settings.get_instance_status",
		callback: function (r) {
			if (r.message) {
				instance_manager.render(r.message);
			}
		},
	});
};

instance_manager.render = function (status) {
	$(".instance-expiry-bar").remove();
	$("#instance-suspended-overlay").remove();

	if (status.suspended) {
		instance_manager.show_suspended_overlay(status);
		return;
	}

	let message = "";
	let bar_class = "";
	let icon = "⚠";

	if (status.in_grace) {
		const grace_left = status.grace_days_remaining;
		const since = status.days_since_expiry;
		message =
			`<strong>License Expired – Grace Period Active:</strong> ` +
			`Expired <strong>${since}</strong> day(s) ago. ` +
			`<strong>${grace_left}</strong> grace day(s) remaining before suspension. ` +
			`Please contact your administrator.`;
		bar_class = "instance-bar-danger";
		icon = "⛔";
	} else if (status.days_remaining <= 7) {
		message =
			`<strong>License Expiring Soon!</strong> ` +
			`Only <strong>${status.days_remaining}</strong> day(s) left — expires on <strong>${status.expiry_date}</strong>. ` +
			`Please renew your license.`;
		bar_class = "instance-bar-warning";
	} else if (status.days_remaining <= 30) {
		message =
			`<strong>License Expiry Notice:</strong> ` +
			`<strong>${status.days_remaining}</strong> days remaining until expiry on <strong>${status.expiry_date}</strong>.`;
		bar_class = "instance-bar-info";
	} else {
		return;
	}

	const bar_html = `
		<div class="instance-expiry-bar ${bar_class}">
			<span class="bar-icon">${icon}</span>
			<span class="bar-message">${message}</span>
		</div>`;

	$(".layout-main-section").before(bar_html);
};

instance_manager.show_suspended_overlay = function (status) {
	const since = status.days_since_expiry;
	const expiry_date = status.expiry_date;
	const grace_days = status.grace_period_days;

	const overlay_html = `
		<div id="instance-suspended-overlay">
			<div class="suspended-card">
				<div class="suspended-lock">🔒</div>
				<h2 class="suspended-title">Instance Suspended</h2>
				<p class="suspended-sub">Access to this instance has been disabled.</p>
				<div class="suspended-details">
					<p>License expired on <strong>${expiry_date}</strong> (<strong>${since}</strong> day(s) ago).</p>
					<p>Grace period of <strong>${grace_days}</strong> day(s) has ended.</p>
				</div>
				<div class="suspended-contact">
					<p>Please contact your administrator to renew the license and restore access.</p>
				</div>
			</div>
		</div>`;

	$("body").append(overlay_html);
};

$(document).on("page-change", function () {
	instance_manager.load_instance_bar();
});

setInterval(function () {
	instance_manager.load_instance_bar();
}, 5 * 60 * 1000);

// ── User list: block "New" button when all limits are reached ─────────────

(function () {
	var existing = frappe.listview_settings["User"] || {};
	var orig_onload = existing.onload;

	frappe.listview_settings["User"] = Object.assign({}, existing, {
		onload: function (listview) {
			if (orig_onload) orig_onload(listview);

			var orig_make_new = listview.make_new_doc.bind(listview);
			listview.make_new_doc = function () {
				frappe.call({
					method: "instance_manager.instance_manager.instance_manager.doctype.instance_settings.instance_settings.check_new_user_allowed",
					callback: function (r) {
						if (r.message && !r.message.allowed) {
							frappe.msgprint({
								title: __("User Limit Exceeded"),
								message: r.message.reason,
								indicator: "red",
							});
						} else {
							orig_make_new();
						}
					},
				});
			};
		},
	});
})();
