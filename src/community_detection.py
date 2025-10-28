def AllLouv(newP):
    """Run multiple Louvain community detections with random node shuffling
    and return average statistics and best partition."""

    num_iterazioni = 200
    dzNlouv = {}
    Nmod = np.zeros(num_iterazioni)
    Nnumc = np.zeros(num_iterazioni)
    mapping = {idx: node for idx, node in enumerate(newP.nodes())}

    for i in range(num_iterazioni):
        numeri_random = random.sample(range(len(newP.nodes())), len(newP.nodes()))
        G_shf = nx.Graph()
        G_shf.add_nodes_from(mapping[numero] for numero in numeri_random)
        G_shf.add_edges_from(newP.edges())

        h = list(louvain_communities(G_shf))
        Nh = len(h)
        modh = modularity(G_shf, h, resolution=1)

        dzNlouv[i] = h
        Nmod[i] = modh
        Nnumc[i] = Nh

    idxmax = np.argmax(Nmod)
    modmax = Nmod[idxmax]
    numcompmodmax = int(Nnumc[idxmax])

    print("\nBest partition:\n", dzNlouv[idxmax], modularity(G_shf, dzNlouv[idxmax], resolution=1))
    print(idxmax, modmax, Nmod[idxmax], Nnumc[idxmax])

    modmed = np.mean(Nmod)
    errmodmed = np.std(Nmod) / np.sqrt(len(Nmod))
    compmed = np.mean(Nnumc)
    errcompmed = np.std(Nnumc) / np.sqrt(len(Nnumc))

    partizmax = {j: list(dzNlouv[idxmax][j]) for j in range(numcompmodmax)}

    print("\nAverage values:\n")
    print(modmed, errmodmed)
    print(compmed, errcompmed)

    return modmed, errmodmed, compmed, errcompmed, modmax, numcompmodmax, partizmax

