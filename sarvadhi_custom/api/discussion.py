import frappe
 
@frappe.whitelist(allow_guest=True)
def get_announcements(channel=None, page=1, limit=None):  # Set default limit to 5
    filters = {"published": 1}
    if channel:
        filters["type_of_announcement"] = channel  # Use type_of_announcement instead of discussion_channel
 
    # Calculate the start index for pagination
    start = (int(page) - 1) * int(limit)
 
    announcements = frappe.get_all(
        "Sarvadhi Announcements",
        fields=["name", "announcement_name", "description", "created_by", "creation"],
        filters=filters,
        order_by="creation desc",
        start=start,
        page_length=int(limit)
    )
 
    # Fetch total count of announcements for pagination
    total_count = frappe.db.count("Sarvadhi Announcements", filters=filters)
 
    # Fetch reactions and attachments for each announcement
    for announcement in announcements:
        # Fetch reactions
        reactions = frappe.get_all(
            "User Table For Announcement",
            filters={"parent": announcement["name"]},
            fields=["user", "reaction"]
        )
        announcement["reactions"] = reactions  # Include individual reactions for user-specific highlighting
 
        # Fetch attachments
        attachments = frappe.get_all(
            "File",
            filters={
                "attached_to_doctype": "Sarvadhi Announcements",  # Replace with your actual doctype name
                "attached_to_name": announcement["name"]
            },
            fields=["file_url", "file_name"]  # Include file URL and name
        )
        announcement["attachments"] = [
            {
                "url": attachment.file_url,
                "name": attachment.file_name
            } for attachment in attachments
        ]
        print("Attachments fetched:", announcement["attachments"])
 
        # Convert datetime objects to strings
        if announcement.get("creation"):
            announcement["creation"] = announcement["creation"].isoformat()
 
    return {
        "message": announcements,
        "total_count": total_count,
        "page": int(page),
        "limit": int(limit)
    }
 
 
 
 
@frappe.whitelist(allow_guest=True)
def fetch_channels():
    try:
        user = frappe.session.user
        channels = frappe.get_all(
            "Discussion Channel",
            fields=["name", "channel_name"],
            filters=[["Members", "user", "=", user]]
        )
        return channels
 
    except Exception as e:
        return {"error": "An error occurred while fetching channels."}
 
 
@frappe.whitelist(allow_guest=True)
def update_reaction(post_id=None, emoji=None):
    data = frappe.form_dict  # Capture all request data
  
    post_id = data.get("post_id")
    emoji = data.get("emoji")
 
    if not post_id:
        frappe.throw("Post ID is required")
 
    user = frappe.session.user  # Get the logged-in user
 
    # Fetch the parent document (Sarvadhi Announcements)
    announcement = frappe.get_doc("Sarvadhi Announcements", post_id)
 
    # Check if the user already has a reaction
    existing_reaction = None
    for reaction in announcement.reactions:
        if reaction.user == user:
            existing_reaction = reaction
            break
 
    if existing_reaction:
        # Update the existing reaction
        existing_reaction.reaction = emoji
    else:
        # Append a new reaction
        announcement.append("reactions", {
            "user": user,
            "reaction": emoji
        })
 
    # Save the document
    announcement.save()
    frappe.db.commit()
 
    return {"status": "success"}
 
def set_created_by(doc, method):
    username = frappe.db.get_value("User", frappe.session.user, "username")
    doc.created_by = username if username else frappe.session.user
 


@frappe.whitelist(allow_guest=True)
def get_users_by_role(roles):
    if isinstance(roles, str):
        roles = frappe.parse_json(roles)  # Convert JSON string to list
 
    print("Fetching users with roles:", roles)
 
    user_links = frappe.get_all(
        "Has Role",
        filters={"role": ["in", roles]},
        fields=["parent"]
    )
 
    user_ids = list(set(user["parent"] for user in user_links))  # Remove duplicates
 
    users = frappe.get_all(
        "User",
        filters={"name": ["in", user_ids]},
        fields=["name", "username"]
    )
 
    print("Users fetched:", users)
    return users
 
 