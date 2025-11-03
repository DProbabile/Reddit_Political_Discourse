#label_colors.py

# ======================
# LABEL ASSIGNMENT
# ======================

def Label_from_list(lista, DizValTag):
    """
    Assigns a combined label to a community based on tag contributions.

    Parameters
    ----------
    lista : list
        List of subreddit names belonging to the community.
    DizValTag : dict
        Mapping 'tag_subreddit' -> value (e.g., 'Left_politics': 0.8).

    Returns
    -------
    res : str
        Combined label (e.g., "Cons/Politic").
    """
    PurTh = 0.5
    PolTh = 10
    AbsTh = 0

    dizntag = {}
    politic = 0

    for col in csvdf2.columns[1:]:
        dizntag[col] = 0

    for i in lista:
        for col in csvdf2.columns[1:]:
            key = f"{col}_{i}"
            if key in DizValTag:
                if col != "Politic":
                    dizntag[col] += DizValTag[key]
                else:
                    politic += DizValTag[key]

    MAX = max(dizntag, key=dizntag.get)
    res = MAX
    dizntag["Politic"] = politic

    rank = {}
    for col in csvdf2.columns[1:]:
        if dizntag[col] >= PurTh * dizntag[MAX] and col != MAX and dizntag[col] >= AbsTh:
            rank[col] = dizntag[col]

    Others = sorted(rank, key=rank.get, reverse=True)
    if Others:
        for o in Others:
            if o != "Politic":
                res += f"/{o}"
        if len(Others) <= PolTh and "Politic" in Others:
            res += "/Politic"

    return res



# ======================
# COLOR ASSIGNMENT
# ======================

# ======================
# COLOR ASSIGNMENT
# ======================

def Color_from_list(lista, DizValTag):
    """
    Assigns a representative color to a community based on tag contributions.

    Parameters
    ----------
    lista : list
        List of subreddit names in the community.
    DizValTag : dict
        Mapping 'tag_subreddit' -> weight value.

    Returns
    -------
    colore_somma_pesato : tuple
        Weighted RGB color of the community.
    """
    PurTh = 0.5
    PolTh = 10
    AbsTh = 0

    dizntag = {}
    politic = 0
    colori_pesati = []

    for col in csvdf2.columns[1:]:
        dizntag[col] = 0

    for i in lista:
        for col in csvdf2.columns[1:]:
            key = f"{col}_{i}"
            if key in DizValTag:
                if col != "Politic":
                    dizntag[col] += DizValTag[key]
                else:
                    politic += DizValTag[key]

    MAX = max(dizntag, key=dizntag.get)
    colori_pesati.append((Color_Field[MAX], dizntag[MAX]))
    dizntag["Politic"] = politic

    rank = {}
    for col in csvdf2.columns[1:]:
        if dizntag[col] >= PurTh * dizntag[MAX] and col != MAX and dizntag[col] >= AbsTh:
            rank[col] = dizntag[col]

    Others = sorted(rank, key=rank.get, reverse=True)
    if Others:
        for o in Others:
            if o != "Politic":
                colori_pesati.append((Color_Field[o], dizntag[o]))
        if len(Others) <= PolTh and "Politic" in Others:
            colori_pesati.append((Color_Field["Politic"], dizntag["Politic"] * 0.1))

    return somma_colori_pesati(colori_pesati)
