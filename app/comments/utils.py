# app/comments/utils.py

def build_comment_tree(comments):
    comment_map = {}
    roots = []

    # Prepare comment map
    for comment in comments:
        comment["replies"] = []
        comment_map[comment["id"]] = comment

    # Build nested structure
    for comment in comments:
        parent_id = comment["parent_id"]

        if parent_id:
            parent = comment_map.get(parent_id)

            if parent:
                parent["replies"].append(comment)
        else:
            roots.append(comment)

    return roots