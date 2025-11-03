# ============================================
# echo_chamber_matrix.py
# ============================================

# ======================
# ECHO CHAMBER MATRIX
# ======================

def calculate_overlap_list(user_cluster, domain_cluster):
    """
    Compute the overlap (intersection) between two subreddit clusters.

    Parameters
    ----------
    user_cluster : list
        Subreddits in the user-based community.
    domain_cluster : list
        Subreddits in the domain-based community.

    Returns
    -------
    list
        List of overlapping subreddits.
    """
    return list(set(user_cluster).intersection(set(domain_cluster)))


def assign_users_to_blocks(list_matrix_ec, user_dict):
    """
    Assign users to (i, j) blocks of the echo chamber matrix based on subreddit membership.

    Parameters
    ----------
    list_matrix_ec : dict
        Nested dictionary of subreddit intersections for each (i, j) pair.
    user_dict : dict
        Mapping user → [list_of_subreddits, activity_count].

    Returns
    -------
    User_list_matrix_ec : dict
        Nested dictionary where each (i, j) contains the list of users assigned to that block.
    """
    subreddit_index = {}
    for i, inner_dict in list_matrix_ec.items():
        for j, subreddit_list in inner_dict.items():
            for sub in subreddit_list:
                subreddit_index.setdefault(sub, []).append((i, j))

    User_list_matrix_ec = {i: {j: [] for j in inner_dict.keys()} for i, inner_dict in list_matrix_ec.items()}

    for user, data in user_dict.items():
        if not data:
            continue
        user_subreddits = data[0]
        for sub in user_subreddits:
            if sub in subreddit_index:
                for (i, j) in subreddit_index[sub]:
                    User_list_matrix_ec[i][j].append(user)

    return User_list_matrix_ec

