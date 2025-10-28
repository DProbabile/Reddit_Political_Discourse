# Polarization and Echo Chambers in Reddit’s Political Discourse

**Cirulli, Desiderio, Cimini, Saracco (2025)**  
*Polarization and echo chambers in Reddit’s political discourse.*

This repository provides the computational framework used in the study.  
We analyse Reddit political discussions (2013–2017) through bipartite networks linking
users, subreddits, and external domains.  
Statistically validated projections (BiCM/BiWCM) reveal the structure of political
communities and the formation of echo chambers across interaction and information layers.

## Repository structure


Reddit_Political_Discourse/
│
├── README.md
├── requirements.txt
│
├── data/
│ ├── sample_subset/ # <--- minimal dataset for replication 
│ │ ├── users_subreddits_subset.parquet
│ │ └── subreddits_domains_subset.parquet
│ └── (no raw Reddit data included)
│
├── src/ # core modules (your code)
│ ├── label_colors.py
│ ├── community_detection.py
│ ├── polarization_metrics.py
│ ├── echo_chamber_matrix.py
│ ├── distance_in_network.py
│ └── utils.py
│
├── notebooks/
│ ├── 00_quickstart.ipynb # example pipeline using subset data
│ ├── 01_polarizarion_analysis.ipynb
│ ├── 02_echo_chamber_validation.ipynb
│ └── 03_distance_analysis.ipynb
│
└── figures/ # optional plots generated in notebooks


---

## Overview

The analysis is based on two complementary bipartite layers:

1. **Interaction layer (users–subreddits):**  
   Captures how users participate in political discussions across communities.

2. **Information layer (subreddits–domains):**  
   Describes how subreddits link to external information sources and news outlets.

Both layers are statistically validated using maximum-entropy null models (BiCM/BiWCM),  
ensuring that observed correlations are not due to degree heterogeneity alone.  
Community detection and overlap analysis reveal how interaction and information patterns
jointly shape echo chambers and political polarization.

---

## Function overview

This section briefly outlines the role of the main functions provided in `src/`.  
You can expand this area with additional notes or usage examples.

| Module | Purpose |
|--------|----------|
| `label_colors.py` | Maps community tags to consistent color schemes |
| `community_detection.py` | Runs Louvain / Infomap / SBM; supports consensus and relabeling |
| `polarization_metrics.py` | Computes user polarization metrics (e.g., polarization index ρ, tag distributions) |
| `echo_chamber_matrix.py` | Builds overlap matrices between user and domain communities; validates overlaps via BiWCM |
| `distance_in_network.py` | Computes distances between validated subnetworks or user groups |
| `utils.py` | Helper functions: normalization dictionaries, FDR correction, reproducibility controls |


## Analysis pipeline

1. **Data import and filtering**  
   - Load Reddit Politosphere and Pushshift datasets; restrict to political subreddits.  
   - Apply RCA normalization and build bipartite matrices (users–subreddits, subreddits–domains).

2. **Validated projections**  
   - Perform BiCM/BiWCM validation (FDR correction) to retain significant co-occurrences.

3. **Community detection**  
   - Identify political communities (Louvain / Infomap / SBM).

4. **Polarization metrics**  
   - Compute polarization index ρ and participation asymmetries.

5. **Echo-chamber validation**  
   - Measure overlaps between interaction and information communities using BiWCM.

6. **Statistical testing and visualization**  
   - Apply KS and Mann–Whitney tests; visualize partitions and matrices.


## 📚 Data availability

All data used in this study are publicly available:

- **Reddit Politosphere dataset (2013–2017)**  
  [https://zenodo.org/record/5154892](https://zenodo.org/record/5154892)

- **Pushshift Reddit archives**  
  [https://pushshift.io](https://pushshift.io)

Raw Reddit data are **not included** in this repository.


##  Data subsets for replication

To facilitate replication without accessing the full Reddit datasets,  
this repository includes small preprocessed subsets and auxiliary structures under `data/sample_subset/`.

###  Files

| File | Description |
|------|--------------|
| `users_subreddits_subset.parquet` | Bipartite user–subreddit interactions (comments or participation counts) |
| `subreddit_labels.df` | Mapping of subreddits → political tag (e.g. Democrat, Republican, Banned, Neutral) |
| `color_dict.json` | Color scheme associated with subreddit/community tags |
| `user_normalization_dict.json` | Auxiliary dictionary for normalization or RCA binarization parameters |

These files reproduce the internal structure used in the paper’s code base,  
allowing all notebooks to run on a small, representative example.


### Example structures

**Example — user–subreddit bipartite data**

| user_id | subreddit | num. comments | RCA 
|----------|------------|----------|-----|
| u12345   | politics   | 42       | 1.21 | 
| u45678   | The_Donald | 58       | 1.45 | 
| u91011   | worldnews  | 6        | 0.98 | 

**Example 3 — auxiliary dictionaries**

```json
{
  "user_subreddits": {
    "u12345": ["politics", "hillaryclinton", "worldnews"],
    "u45678": ["The_Donald", "conservative", "AskTrumpSupporters"],
    "u91011": ["socialism", "progressive", "NeutralPolitics"]
  },
  "subreddit_labels": {
    "politics": "Democrat",
    "hillaryclinton": "Democrat",
    "The_Donald": "Conservative",
    "conservative": "Conservative",
    "socialism": "Far-Left",
    "progressive": "Left",
    "NeutralPolitics": "Neutral",
    "worldnews": "Neutral"
  }
}
```

Each key corresponds to a structure used in the analysis:  
- `user_subreddits`: dictionary mapping each user ID to the list of subreddits they commented on.  
- `subreddit_labels`: mapping from subreddit name to political tag (e.g., Democrat, Conservative, Far-Left, Neutral).  

These subsets are illustrative, not exhaustive.  
They reproduce the schema and naming conventions used in the full datasets  
and can be extended seamlessly for large-scale analyses.  
If you create additional subsets (for example, per year or by domain category),  
please document them here using the same template.

---

## External methods and references

- Statistical validation:  
  - [bicm](https://pypi.org/project/bicm/) – for unweighted bipartite networks (BiCM)  
  - BiWCM module (weighted validation) – custom implementation used in this paper, not yet public.  
    It extends BiCM to weighted bipartite projections; contact authors for access or replication details.  

- RCA filtering: activity normalization before validation  
- Community detection: [NetworkX](https://networkx.org/), [igraph](https://igraph.org/python/), [Infomap](https://www.mapequation.org/), [graph-tool](https://graph-tool.skewed.de/)  
- Statistical tests: [SciPy](https://scipy.org/)  
- Visualization: Matplotlib, Plotly, Sankey diagrams, chord plots  

---

## Reproducibility notes

Random seeds fixed for community detection.  
FDR correction applied to validated links and overlap matrices.  
Results consistent across detection algorithms (Louvain, Infomap, SBM).  
BiWCM implementation available upon request for reproducibility purposes.

---

## Citation

If you use this code, please cite:

```
@article{CirulliEtAl2025_RedditPolarization,
  title   = {Polarization and Echo Chambers in Reddit’s Political Discourse},
  author  = {Cirulli, Daniele and Desiderio, Antonio and Cimini, Giulio and Saracco, Fabio},
  year    = {2025},
  journal = {arXiv preprint},
  note    = {arXiv:to-be-added}
}
```

