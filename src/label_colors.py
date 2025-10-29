
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
        Dictionary mapping tag_subreddit -> value (e.g., 'Left_politics': 0.8).

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

    # initialize tags
    for col in csvdf2.columns[1:]:
        dizntag[col] = 0

    # accumulate tag weights
    for i in lista:
        for col in csvdf2.columns[1:]:
            if f"{col}_{i}" in DizValTag:
                if col != "Politic":
                    dizntag[col] += DizValTag[f"{col}_{i}"]
                else:
                    politic += DizValTag[f"{col}_{i}"]

    MAX = max(dizntag, key=dizntag.get)
    res = MAX
    dizntag["Politic"] = politic
    T = False
    Others = []
    rank = {}

    for col in csvdf2.columns[1:]:
        if dizntag[col] >= PurTh * dizntag[MAX] and col != MAX:
            if dizntag[col] >= AbsTh:
                rank[col] = dizntag[col]
                T = True

    for col in sorted(rank, key=rank.get, reverse=True):
        Others.append(col)

    if T:
        for o in Others:
            if o != "Politic":
                res += f"/{o}"
        if len(Others) <= PolTh and "Politic" in Others:
            res += "/Politic"
        return res
    else:
        return res


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
        Mapping of tag_subreddit to contribution weight.

    Returns
    -------
    colore_somma_pesato : tuple (R, G, B)
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
            if f"{col}_{i}" in DizValTag:
                if col != "Politic":
                    dizntag[col] += DizValTag[f"{col}_{i}"]
                else:
                    politic += DizValTag[f"{col}_{i}"]

    MAX = max(dizntag, key=dizntag.get)
    colori_pesati.append((Color_Field[MAX], dizntag[MAX]))
    dizntag["Politic"] = politic
    T = False
    Others = []
    rank = {}

    for col in csvdf2.columns[1:]:
        if dizntag[col] >= PurTh * dizntag[MAX] and col != MAX:
            if dizntag[col] >= AbsTh:
                rank[col] = dizntag[col]
                T = True

    for col in sorted(rank, key=rank.get, reverse=True):
        Others.append(col)

    if T:
        for o in Others:
            if o != "Politic":
                colori_pesati.append((Color_Field[o], dizntag[o]))
        if len(Others) <= PolTh and "Politic" in Others:
            colori_pesati.append((Color_Field["Politic"], dizntag["Politic"] * 0.1))
        return somma_colori_pesati(colori_pesati)
    else:
        return somma_colori_pesati(colori_pesati)

