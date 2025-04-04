import frappe

@frappe.whitelist(allow_guest=True)
def update_reaction(post_id=None, emoji=None):
    data = frappe.form_dict  # Capture all request data
    
    frappe.logger().info(f"Received data: {data}")  # Log incoming data

    post_id = data.get("post_id")
    print("post_id:",post_id)
    emoji = data.get("emoji")
    print("emoji:",emoji)

    if not post_id:
        frappe.throw("Post ID is required")
    user = frappe.session.user  # Get the logged-in user
    
    # Check if the user has already reacted
    reaction_entry = frappe.get_all("User Table For Announcement", 
                                    filters={"parent": post_id, "user": user}, 
                                    fields=["name", "reaction"])

    if reaction_entry:
        existing_reaction = reaction_entry[0]["reaction"]
        
        if emoji:
            if existing_reaction != emoji:
                # Update reaction
                frappe.db.set_value("User Table For Announcement", reaction_entry[0]["name"], "reaction", emoji)
        else:
            # Remove reaction
            frappe.delete_doc("User Table For Announcement", reaction_entry[0]["name"])
    else:
        if emoji:
            # Add new reaction
            doc = frappe.get_doc({
                "doctype": "User Table For Announcement",
                "parent": post_id,
                "parentfield": "reactions",
                "parenttype": "Sarvadhi Announcements",
                "user": user,
                "reaction": emoji
            })
            doc.insert()

    # Update the main doctype (Sarvadhi Announcements)
    update_announcement_reactions(post_id)

    frappe.db.commit()
    return {"status": "success"}

def update_announcement_reactions(post_id):
    """Updates the reactions child table in 'Sarvadhi Announcements'."""
    reactions = frappe.get_all("User Table For Announcement",
                               filters={"parent": post_id},
                               fields=["user", "reaction"])

    # Fetch the parent document
    announcement = frappe.get_doc("Sarvadhi Announcements", post_id)

    # Clear existing reactions from the child table
    announcement.reactions = []

    # Append new reactions
    for reaction in reactions:
        announcement.append("reactions", {
            "user": reaction["user"],
            "reaction": reaction["reaction"]
        })

    # Save the document
    announcement.save()
    frappe.db.commit()


@frappe.whitelist()
def get_user_reaction(post_id):
    """Fetch the user's current reaction for a given post."""
    user = frappe.session.user

    reaction_entry = frappe.get_all("User Table For Announcement",
                                    filters={"parent": post_id, "user": user},
                                    fields=["reaction"])

    if reaction_entry:
        return {"reaction": reaction_entry[0]["reaction"]}
    return {"reaction": None}

def set_created_by(doc, method):
    username = frappe.db.get_value("User", frappe.session.user, "username")
    doc.created_by = username if username else frappe.session.user