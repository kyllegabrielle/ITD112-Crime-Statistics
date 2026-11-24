# ITD112 Group 5 — Crime Statistics and Public Safety

## Project scope
Philippine regional crime statistics, 2020–2024. The original data are attributed to **Philippine Statistics Authority (PSA), Table 17.4**, sourced from **Philippine National Police (PNP-CIRAS)**. This supplied CSV was obtained from a third-party mirror; verify source metadata before final submission.

### Data structure
- `data/raw/psa_crime_original.csv`: original supplied CSV, **360 rows** (18 geographic entries x 4 indicators x 5 years).
- `data/processed/crime_clean_long.csv`: cleaned long-format data (360 rows).
- `data/processed/crime_analysis_ready.csv`: tidy wide-format data (90 rows: 85 region-year rows and 5 national totals).
- After running Python, the script saves two cluster data matrices, one raw and one standardized, under `data/processed/`.

**Do not add national totals to the regional records**: this would double-count. Keep the national aggregate for the line plot only.

## Run Python visualizations on macOS (VS Code Terminal)
1. Open this unzipped folder in VS Code.
2. Run:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python python/create_visualizations.py
```
3. Four PNGs appear under `visualizations/python/`.

## Run R visualizations
Install **R** (https://cran.r-project.org/) and then from this project root:
```bash
Rscript -e 'install.packages(c("readr", "dplyr", "tidyr", "ggplot2", "pheatmap"), repos="https://cloud.r-project.org")'
Rscript r/create_visualizations.R
```
Four PNGs appear under `visualizations/r/`. Python must run first to create the standardized clustering matrix used by R.

## Required chart plan
1. Scatterplot: regional monthly crime rates versus crime solution efficiency, 85 region-years.
2. Line plot: national reported total crime incidents across 2020–2024.
3. Heatmap: 17 regions x five years using average monthly crime rates.
4. Cluster map: hierarchical clustering of 17 regional profiles using 10 standardized annual features (5 rates and 5 solution-efficiency values). Ward method with Euclidean distance. This is statistical grouping, **not** a physical hotspot map.

## Deliverables remaining
- Execute R code and verify four R PNGs, compare eight outputs and write interpretations.
- Develop the required dashboard and final case study report; include actual outputs and source code.
- Record package versions, data-source URL, and limitations in final paper.

Official data citation: https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__3S__C17/0041H2BAMC0.px/


## Dashboard and deployment

A responsive React/Vite presentation dashboard is available at `dashboard/`. See `dashboard/README.md` for commands and Netlify/Vercel publishing instructions.
