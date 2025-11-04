# ============================================
# distance_in_network.py
# ============================================

import networkx as nx
import numpy as np
import math

def harmonic_mean_distance(G, node_list1, node_list2=None):
    """
    Compute the harmonic mean distance (1/d) between pairs of nodes.

    Parameters
    ----------
    G : networkx.Graph
        Input graph.
    node_list1 : list
        List of source nodes.
    node_list2 : list, optional
        List of target nodes. If None, uses all pairs within node_list1.

    Returns
    -------
    mean_harm : float
        Harmonic mean distance.
    err_harm : float
        Standard error of the mean.
    """
    if node_list2 is None:
        node_list2 = node_list1

    distances = []
    for i, n1 in enumerate(node_list1):
        targets = node_list2[i + 1:] if node_list1 is node_list2 else node_list2
        for n2 in targets:
            if n1 == n2:
                continue
            if nx.has_path(G, n1, n2):
                d = nx.shortest_path_length(G, n1, n2)
                distances.append(1 / d)
            else:
                distances.append(0)

    if len(distances) == 0:
        return 0, 0

    mean_harm = len(distances) / np.sum(distances)
    err_harm = np.std(distances) / math.sqrt(len(distances))
    return mean_harm, err_harm

