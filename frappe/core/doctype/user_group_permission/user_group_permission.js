// Copyright (c) 2024, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("User Group Permission", {
	setup: (frm) => {
		frm.set_query("allow", () => {
			return {
				filters: {
					issingle: 0,
					istable: 0,
				},
			};
		});

		frm.set_query("applicable_for", () => {
			return {
				query: "frappe.core.doctype.user_group_permission.user_group_permission.get_applicable_for_doctype_list",
				doctype: frm.doc.allow,
			};
		});
	},

	refresh: (frm) => {
		// Can build report in future

		// frm.add_custom_button(__("View Permitted Documents"), () =>
		// 	frappe.set_route("query-report", "Permitted Documents For User Group", {
		// 		user_group: frm.doc.user_group,
		// 	})
		// );

		frm.trigger("set_applicable_for_constraint");
		frm.trigger("toggle_hide_descendants");
	},

	allow: (frm) => {
		if (frm.doc.allow) {
			if (frm.doc.for_value) {
				frm.set_value("for_value", null);
			}
			frm.trigger("toggle_hide_descendants");
		}
	},

	apply_to_all_doctypes: (frm) => {
		frm.trigger("set_applicable_for_constraint");
	},

	set_applicable_for_constraint: (frm) => {
		frm.toggle_reqd("applicable_for", !frm.doc.apply_to_all_doctypes);

		if (frm.doc.apply_to_all_doctypes && frm.doc.applicable_for) {
			frm.set_value("applicable_for", null, null, true);
		}
	},

	toggle_hide_descendants: (frm) => {
		let show = frappe.boot.nested_set_doctypes.includes(frm.doc.allow);
		frm.toggle_display("hide_descendants", show);
	},
});
