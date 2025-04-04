import frappe

@frappe.whitelist(allow_guest=True)
def submit_voting(post_name=None, vote=None):
    print("Submitting vote for post:", post_name, "with vote:", vote)
    doc = frappe.get_doc("Discussion Post", post_name)
# Ensure numerical values for voting fields
    doc.yes_count = int(doc.yes_count or 0)  # Convert to integer if None or string
    doc.no_count = int(doc.no_count or 0)
    doc.total_votes = int(doc.total_votes or 0)
    # Update vote counts
    if vote == "YES":
        doc.yes_count += 1
    elif vote == "NO":
        doc.no_count += 1

    doc.total_votes += 1
    doc.save()
    frappe.db.commit()

    return {"message": "Vote submitted successfully"}



@frappe.whitelist(allow_guest=True)
def get_vote_counts(post_name):
    print("Fetching vote counts for post:", post_name)
    doc = frappe.get_doc("Discussion Post", post_name)
    return {
        "yes_count": doc.yes_count,
        "no_count": doc.no_count
    }





# import frappe

# @frappe.whitelist()
# def submit_reaction(post_name, imogi):
#     try:
#         user = frappe.session.user
#         if user == "Guest":
#             return {"success": False, "message": "Login required"}

#         frappe.logger().info(f"User: {user}, Post: {post_name}, Emoji: {imogi}")

#         # Check if reaction already exists for the same post and user
#         reaction = frappe.get_all("Reaction", filters={"parent": post_name, "user": user, "imogi": imogi}, limit=1)

#         if reaction:
#             reaction_doc = frappe.get_doc("Reaction", reaction[0].name)
#             reaction_doc.count += 1
#             reaction_doc.save()
#         else:
#             reaction_doc = frappe.get_doc({
#                 "doctype": "Reaction",
#                 "parent": post_name,
#                 "parenttype": "Discussion Post",
#                 "parentfield": "reaction",
#                 "user": user,
#                 "imogi": imogi,
#                 "count": 1
#             })
#             reaction_doc.insert()
#         print("Reaction document:", reaction_doc)
#         # Fetch the post document
#         post = frappe.get_doc("Discussion Post", post_name)
#         print("Post fetched:", post)
#         post.reload()
#         # Ensure the 'reactions' child table exists before appending
#         if not post.get("reaction"):
#             post.set("reaction", [])

#         # Avoid duplicate reaction entries in child table
#         existing_reaction = next((r for r in post.reaction if r.user == user and r.imogi == imogi), None)

#         if not existing_reaction:
#             post.append("reaction", {
#                 "imogi": imogi,
#                 "user": user,
#                 "count": reaction_doc.count
#             })

#         post.save(ignore_permissions=True)  # Save the post with new child table entry
#         frappe.db.commit()

#         return {"success": True}

#     except Exception as e:
#         frappe.logger().error(f"Error in submit_reaction: {str(e)}")
#         return {"success": False, "error": str(e)}



# @frappe.whitelist()
# def get_reactions(post_name):
#     reactions = frappe.get_all("Reaction", filters={"parent": post_name}, fields=["emoji", "count"])
    
#     reaction_data = {}
#     for reaction in reactions:
#         reaction_data[reaction["emoji"]] = reaction["count"]

#     return {"success": True, "reactions": reaction_data}





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
