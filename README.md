# Polarization and Echo Chambers in Reddit’s Political Discourse

**Cirulli, Desiderio, Cimini, Saracco (2025)**  
*Polarization and echo chambers in Reddit’s political discourse.*

This repository provides the computational framework used in the study.  
We analyse Reddit political discussions (2013–2017) through bipartite networks linking
users, subreddits, and external domains.  
Statistically validated projections (BiCM/BiWCM) reveal the structure of political
communities and the formation of echo chambers across interaction and information layers.

## Repository structure

```Reddit_Political_Discourse/
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
│ ├── 00_community_characteristics.ipynb 
│ ├── 01_polarizarion_analysis.ipynb
│ ├── 02_echo_chamber_validation.ipynb
│ └── 03_distance_analysis.ipynb
│
└── figures/ -plots generated in notebooks
```
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
   - Load the Reddit Politosphere and Pushshift datasets and restrict the analysis to political subreddits.  
   - Build bipartite matrices (users–subreddits and subreddits–domains) and apply RCA-based binarization to normalize user activity and subreddit popularity.

2. **Validated projections**  
   - Perform BiCM validation (FDR correction) to retain significant co-occurrences.

3. **Community detection**  
   - Identify political communities using Louvain, Infomap, or SBM algorithms.

4. **Polarization metrics**  
   - Compute the polarization index (ρ) both in terms of validated network communities and in terms of groups of subreddits sharing the same topical or ideological tags.

5. **Echo-chamber validation**  
   - Measure overlaps between interaction and information communities by assigning weights to users active in subreddits shared by both communities.  
   - Apply BiWCM-based statistical validation to identify significant overlaps beyond random expectation.

6. **Statistical testing and visualization**  
   - Apply Kolmogorov–Smirnov and Mann–Whitney tests; visualize partitions, polarization matrices, and echo-chamber structures.


## Data availability

All data used in this study are publicly available:

- **Reddit Politosphere dataset (2013–2017)**  
  [The Reddit Politosphere](10.1609/icwsm.v16i1.19377)

- **Pushshift Reddit archives**  
  [https://pushshift.io]([https://pushshift.io](https://arxiv.org/abs/2001.08435))

Raw Reddit data are **not included** in this repository.


##  Data subsets for replication

To facilitate replication without accessing the full Reddit datasets,  
this repository includes small preprocessed subsets and auxiliary structures under `data/sample_subset/`.

###  Files

| File | Description |
|------|--------------|
| `users_subreddits_subset.parquet` | Bipartite user–subreddit interactions (comments or participation counts) |
| `subreddit_labels.df` | Mapping of subreddits → political tag (e.g. Democrat, Republican, Banned...) |
| `user_normalization_dict.json` | Auxiliary dictionary for polarization-normalization |

These files reproduce the internal structure used in the paper’s code base,  
allowing all notebooks to run on a small, representative example.


### Example structures

**Example — user–subreddit bipartite data**

| user_id | subreddit | num. comments 
|----------|------------|----------|
| u12345   | politics   | 42       | 
| u45678   | The_Donald | 58       | 
| u91011   | worldnews  | 6        |  

**Example 2 — auxiliary dictionaries**

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
    It extends BiCM to weighted bipartite projections, following the maximum-entropy formulation  
    introduced in *Buffa et al. (2025), "Maximum entropy modeling of Optimal Transport:  
    the sub-optimality regime and the transition from dense to sparse networks"*  
    ([arXiv:2504.10444](https://arxiv.org/abs/2504.10444)).  
    Contact authors for access or replication details.

- [RCA](https://doi.org/10.1111/j.1467-9957.1965.tb00050.x) filtering: activity normalization before validation 
- [FDR](http://www.jstor.org/stable/2346101) correction
- Community detection: [NetworkX](https://networkx.org/), [igraph](https://igraph.org/python/), [Infomap](https://www.mapequation.org/), [graph-tool](https://graph-tool.skewed.de/)  
- Statistical tests: [SciPy](https://scipy.org/)  
- Visualization: [Matplotlib](https://matplotlib.org), [Plotly](https://plotly.com/python/), [Gephi](http://www.aaai.org/ocs/index.php/ICWSM/09/paper/view/154), [d3blocks](https://github.com/d3blocks/d3blocks)
  

---

## Reproducibility notes

Random seeds fixed for community detection.  
FDR correction applied to validated links and overlap matrices.  
Community detection results consistent across detection algorithms (Louvain, Infomap, SBM[https://graph-tool.skewed.de]).  
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

