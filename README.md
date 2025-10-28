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

