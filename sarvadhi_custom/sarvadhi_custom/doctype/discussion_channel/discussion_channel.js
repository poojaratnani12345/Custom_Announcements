// Copyright (c) 2025, sarvadhi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Discussion Channel", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Discussion Channel", {
    role: function(frm) {
        let selected_roles = frm.doc.role.map(role => role.role);  // Extract role names as an array

        console.log("Selected Roles:", selected_roles);

        if (selected_roles.length > 0) {
            frappe.call({
                method: "sarvadhi_custom.api.channel_api.get_users_by_role",
                args: { roles: selected_roles },  // Pass array of roles
                callback: function(response) {
                    if (response.message) {
                        let users = response.message;
                        console.log("Users with these roles:", users);

                        frm.clear_table("members");

                        let added_users = new Set(); // To prevent duplicate users

                        users.forEach(user => {
                            if (!added_users.has(user.name)) {
                                let row = frm.add_child("members");
                                row.user = user.name;
                                row.username = user.username;
                                added_users.add(user.name);
                            }
                        });

                        frm.refresh_field("members");
                    }
                }
            });
        }
    }
});
