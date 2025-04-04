import frappe

def get_context(context):
    channel_name = frappe.form_dict.get("name")

    if not channel_name:
        frappe.throw("Channel name is required")

    # Fetch all channels for the sidebar
    context.channels = frappe.get_all("Discussion Channel", fields=["name", "channel_name"])

    # Fetch the selected channel details
    context.channel = frappe.get_doc("Discussion Channel", channel_name)

    # Fetch posts of the selected channel
    context.posts = frappe.get_all(
        "Sarvadhi Announcements",
        filters={"type_of_announcement": channel_name},  # 🛠 Fix: Use "channel"
        fields=["*"]
    )






@frappe.whitelist()
def get_user_channels():
    user = frappe.session.user  

    user_channels = frappe.get_all(
        "Members",
        filters={"user": user},
        pluck="parent"
    )

    if not user_channels:
        return []

    # Fetch channel details
    channels = frappe.get_all(
        "Discussion Channel",
        filters={"name": ["in", user_channels]},
        fields=["name"]
    )

    return channels


# postcards = frappe.get_all("Sarvadhi Announcements",
#         filters={"published": 1},
#         fields=["name","announcement_name","subject", "description","created_by"],
#         order_by="creation desc",
#         limit_page_length=10
#     )

#     context.postcards = postcards 
    
#     return context
