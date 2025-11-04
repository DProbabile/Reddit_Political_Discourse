# ============================================
# utils.py
# ============================================


# ======================
# RCA BINARIZATION
# ======================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import plotly.graph_objects as go
import sys 
from pathlib import Path

FIGS = Path(__file__).resolve().parents[1] / "figures"



def rca(matrix):
    world = np.sum(matrix, 0) / np.sum(matrix)
    return np.array([(row / sum(row)) / world for row in matrix])

def RCA_binarize(exp_mat, threshold=1):
    return np.array(np.where(rca(exp_mat) > threshold, 1, 0))

# ======================
# COLOR UTILITIES
# ======================

def plot_colore(colore, colore_esadecimale=None):
    """Plot a color block with optional hex label."""
    plt.figure(figsize=(2, 2))
    plt.bar([0], [1], color=[colore], width=1)
    plt.axis('off')
    if colore_esadecimale:
        plt.title(colore_esadecimale, fontsize=14)
    plt.show()


def nome_colore_to_esadecimale(nome_colore):
    """Convert color name to hex."""
    return mcolors.to_hex(nome_colore)


def somma_colori_pesati(colori_pesati):
    """Compute the weighted average of multiple colors."""
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
    """Convert RGB color or name to hexadecimal."""
    try:
        return mcolors.to_hex(rgb)
    except ValueError:
        return rgb  # already hex


def ordina_legenda(labels, colors, ordine):
    """
    Order legend labels and colors according to thematic priority.
    """
    ordine_map = {k: i for i, k in enumerate(ordine)}
    items = []
    for lab, col in zip(labels, colors):
        first = lab.split("/")[0]
        idx = ordine_map.get(first, len(ordine))
        items.append((idx, lab, col))

    items_sorted = sorted(items, key=lambda x: x[0])
    new_labels = [lab for _, lab, _ in items_sorted]
    new_colors = [col for _, _, col in items_sorted]
    return new_labels, new_colors


# ======================
# RADAR PLOT
# ======================

def plot_diagramma_radar_multiple(liste_valori, colori, labels, titolo):
    """Plot multiple radar charts using Plotly."""
    if not liste_valori:
        raise ValueError("liste_valori cannot be empty.")

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
        title=dict(text=titolo, x=0.5, y=0.96, xanchor='center', font=dict(size=20)),
        polar=dict(radialaxis=dict(visible=True, range=[0, max_range * 1.1])),
        showlegend=True,
        legend=dict(x=1.10, y=1, xanchor="left", yanchor="top", font=dict(size=12)),
        width=850,
        height=650
    ) #save Interaction_Radar_2013.pdf
    fig.write_image(FIGS / "Interaction_Radar_2013.pdf")
    fig.show()


def Radar_from_list(lista, DizValTag):
    """Compute radar values for a given community."""
    dizntag = {}
    for col in csvdf2.columns[1:]:
        dizntag[col] = 0
    for i in lista:
        for col in csvdf2.columns[1:]:
            if f"{col}_{i}" in DizValTag:
                dizntag[col] += DizValTag[f"{col}_{i}"]
    return dizntag


# ======================
# PAPER-STYLE LEGEND
# ======================

def crea_legenda_verticale_paper(
    labels,
    colors,
    output_file=None,
    larghezza_figura=6,
    altezza_unitaria=0.75,
    frameon=False,
    dimensione_font=14,
):
    """Create a vertical color legend for papers."""
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
        print(f"Legenda saved to: {output_file}")
    plt.close()
