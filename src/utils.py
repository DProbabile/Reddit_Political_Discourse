# ======================
# RCA Binarization
# ======================

def rca(matrix):
    world = np.sum(matrix,0)/np.sum(matrix)
    return np.array([(row/sum(row))/world for row in matrix])

def RCA_binarize(exp_mat, threshold = 1):
    return np.array(np.where(rca(exp_mat) > threshold, 1, 0))

# ======================
# COLOR UTILITIES
# ======================

def plot_colore(colore, colore_esadecimale=None):
    """
    Plot a color block with optional hex code label.
    """
    plt.figure(figsize=(2, 2))
    plt.bar([0], [1], color=[colore], width=1)
    plt.axis('off')
    if colore_esadecimale:
        plt.title(colore_esadecimale, fontsize=14)
    plt.show()


def nome_colore_to_esadecimale(nome_colore):
    """
    Convert a color name to hexadecimal format.
    """
    return mcolors.to_hex(nome_colore)


def somma_colori_pesati(colori_pesati):
    """
    Compute the weighted average of a list of colors.

    Parameters
    ----------
    colori_pesati : list of (color, weight)

    Returns
    -------
    colore_somma : tuple (R, G, B)
    """
    r = g = b = peso_totale = 0
    for colore, peso in colori_pesati:
        rgb = mcolors.to_rgb(colore)
        r += rgb[0] * peso
        g += rgb[1] * peso
        b += rgb[2] * peso
        peso_totale += peso

    if peso_totale == 0:
        return (0, 0, 0)

    r /= peso_totale
    g /= peso_totale
    b /= peso_totale
    return (r, g, b)




def rgb_to_hex(rgb):
    """
    Converte un colore RGB o nome in formato esadecimale.
    """
    try:
        return mcolors.to_hex(rgb)
    except ValueError:
        return rgb  # se già esadecimale


def ordina_legenda(labels, colors, ordine):
    """
    Ordina le legende e i colori secondo un ordine tematico definito.

    Parametri
    ----------
    labels : list
        Etichette delle community (es. 'Far-Left/Politic', 'Cons/Lib')
    colors : list
        Colori corrispondenti
    ordine : list
        Lista di priorità (es. ["Geop", "News", "Far-Left", ...])

    Ritorna
    -------
    new_labels, new_colors : tuple di liste ordinate
    """
    ordine_map = {k: i for i, k in enumerate(ordine)}

    items = []
    for lab, col in zip(labels, colors):
        first = lab.split("/")[0]  # prendi la prima parola dell'etichetta
        idx = ordine_map.get(first, len(ordine))  # se non trovata → fine lista
        items.append((idx, lab, col))

    # ordina per indice mantenendo ordine relativo
    items_sorted = sorted(items, key=lambda x: x[0])

    new_labels = [lab for _, lab, _ in items_sorted]
    new_colors = [col for _, _, col in items_sorted]
    return new_labels, new_colors


# ======================================================
# 🔹 Radar Plot
# ======================================================

def plot_diagramma_radar_multiple(liste_valori, colori, labels, titolo):
    """
    Plotta più liste di valori come diagrammi radar utilizzando Plotly.

    Parametri
    ----------
    liste_valori : list of dict
        Ogni elemento è un dizionario {categoria: valore} per una community.
    colori : list
        Lista dei colori (RGB o esadecimali).
    labels : list
        Etichette corrispondenti (es. nomi delle community).
    titolo : str
        Titolo del grafico.
    """
    if not liste_valori:
        raise ValueError("liste_valori non può essere vuota.")

    categories = list(liste_valori[0].keys())
    max_range = max(max(vals.values()) for vals in liste_valori)

    fig = go.Figure()

    for valori, colore, label in zip(liste_valori, colori, labels):
        fig.add_trace(go.Scatterpolar(
            r=list(valori.values()),
            theta=categories,
            fill='toself',
            name=label,
            line=dict(color=rgb_to_hex(colore), width=2)
        ))

    fig.update_layout(
        title=dict(
            text=titolo,
            x=0.5,
            y=0.96,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_range * 1.1]
            )
        ),
        showlegend=True,
        legend=dict(
            x=1.10, y=1,
            xanchor="left",
            yanchor="top",
            font=dict(size=12)
        ),
        width=850,
        height=650
    )

    fig.show()


def Radar_from_list(lista, DizValTag):
    """
    Calcola il dizionario dei valori radar per una community.
    """
    dizntag = {}
    for col in csvdf2.columns[1:]:
        dizntag[col] = 0
    for i in lista:
        for col in csvdf2.columns[1:]:
            if col + "_" + i in DizValTag:
                dizntag[col] += DizValTag[col + "_" + i]
    return dizntag


def crea_legenda_verticale_paper(
    labels,
    colors,
    output_file=None,
    larghezza_figura=6,
    altezza_unitaria=0.75,
    frameon=False,
    dimensione_font=14,
):
    """
    Crea una legenda verticale stile 'paper' con rettangoli colorati.
    Salva in PDF se viene passato output_file.
    """
    handles = [
        mpatches.Patch(edgecolor='black', linewidth=0.6, facecolor=c, label=l)
        for l, c in zip(labels, colors)
    ]
    h = max(1.0, len(labels) * altezza_unitaria)

    plt.figure(figsize=(larghezza_figura, h), dpi=300)
    leg = plt.legend(
        handles=handles,
        loc="center",
        ncol=1,
        frameon=frameon,
        fontsize=dimensione_font,
        labelspacing=0.6,
        handlelength=1.4,
        handleheight=0.9,
        borderpad=0.4,
        handletextpad=0.8,
        columnspacing=1.0,
    )
    if leg and not frameon:
        leg.get_frame().set_linewidth(0.0)
    plt.axis("off")

    if output_file:
        # plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"Legenda salvata in: {output_file}")
    # plt.show()
    plt.close()

