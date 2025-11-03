# ============================================
# polarization_metrics.py
# ============================================

def compute_polarization_matrix(user_data, TAGS, tag_idx, valori_normtag_valid, TagvaluesPerYear, year_label="unknown"):
    """
    Compute the polarization matrix for a set of users and topic tags.

    Parameters
    ----------
    user_data : dict
        Mapping user → (list of subreddits, number of subreddits).
    TAGS : list
        List of thematic tags.
    tag_idx : dict
        Mapping tag → index.
    valori_normtag_valid : dict
        Normalized values for each tag (e.g. number of validated subreddits).
    TagvaluesPerYear : dict
        Mapping tag → list of associated subreddits.
    year_label : str or int, optional
        Label used for progress bar and output.

    Returns
    -------
    dict
        {
            "IndexPolarization": raw matrix,
            "IndexPolarizationNORMALIZED": normalized matrix,
            "DizVectorUser": user–tag vectors,
            "DizLabelUser": assigned labels,
            "partecipanti": participation counts,
            "Utentinonnulli": number of active users,
            "Nmassimi": number of maxima
        }
    """
    DizVectorUser = {}
    DizLabelUser = {}
    partecipanti = [0] * len(TAGS)
    IndexPolarization = np.zeros((len(TAGS), len(TAGS)))
    Utentinonnulli = 0
    Nmassimi = 0

    for user, (subreddit_array, num_subreddits) in tqdm(
        user_data.items(),
        total=len(user_data),
        desc=f"Computing polarization ({year_label})"
    ):
        if not subreddit_array:
            continue

        DizVectorUser[user] = np.zeros(len(TAGS))

        for tag in TAGS:
            if valori_normtag_valid[tag] == 0:
                continue
            inters = len(np.intersect1d(subreddit_array, TagvaluesPerYear[tag])) / (
                num_subreddits * valori_normtag_valid[tag]
            )
            DizVectorUser[user][tag_idx[tag]] = inters

        if np.sum(DizVectorUser[user]) == 0:
            DizLabelUser[user] = np.nan
            continue

        Utentinonnulli += 1
        max_value = np.max(DizVectorUser[user])
        max_indices = np.where(DizVectorUser[user] == max_value)[0]
        Nmassimi += len(max_indices)
        DizLabelUser[user] = list(max_indices)

        for cluster, value in enumerate(DizVectorUser[user]):
            if value != 0:
                partecipanti[cluster] += 1
                for idx in max_indices:
                    IndexPolarization[cluster][idx] += 1 / len(max_indices)

    IndexPolarizationNORMALIZED = copy.deepcopy(IndexPolarization)
    for i in range(len(TAGS)):
        for j in range(len(TAGS)):
            if partecipanti[i] != 0:
                IndexPolarizationNORMALIZED[i][j] /= partecipanti[i]

    print(f"\n✅ Processed {len(DizVectorUser)} users ({Utentinonnulli} active)")
    print("Polarization matrix shape:", IndexPolarization.shape)

    return {
        "IndexPolarization": IndexPolarization,
        "IndexPolarizationNORMALIZED": IndexPolarizationNORMALIZED,
        "DizVectorUser": DizVectorUser,
        "DizLabelUser": DizLabelUser,
        "partecipanti": partecipanti,
        "Utentinonnulli": Utentinonnulli,
        "Nmassimi": Nmassimi
    }

