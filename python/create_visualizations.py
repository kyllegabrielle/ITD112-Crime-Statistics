"""ITD112 Group 5: Philippine crime statistics, four required Seaborn charts.
Run from project root: python python/create_visualizations.py
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data/processed/crime_analysis_ready.csv'
OUT = BASE / 'visualizations/python'
OUT.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA)
df['year'] = df['year'].astype(int)
# Keep national total out of cross-region analysis to avoid double-counting.
regional = df.loc[df['region'] != 'Philippines'].copy()
national = df.loc[df['region'] == 'Philippines'].sort_values('year').copy()
assert len(regional)==85 and len(national)==5, 'Unexpected dataset coverage'
sns.set_theme(style='whitegrid', context='notebook', font_scale=0.98)

# 1. SCATTERPLOT: regional rate versus solution efficiency; 85 region-years.
fig, ax = plt.subplots(figsize=(10,6.5))
sns.scatterplot(data=regional, x='average_monthly_crime_rate', y='crime_solution_efficiency_pct',
                hue='year', palette='viridis', s=85, alpha=.87, edgecolor='white', linewidth=.6, ax=ax)
ax.set(title='Regional Crime Rate vs. Crime Solution Efficiency (2020–2024)',
       xlabel='Average monthly crime rate (per 100,000 population)',
       ylabel='Crime solution efficiency (%)')
ax.legend(title='Year', bbox_to_anchor=(1.02,1), loc='upper left')
fig.tight_layout();fig.savefig(OUT/'01_scatterplot.png',dpi=220,bbox_inches='tight');plt.close(fig)

# 2. LINE PLOT: use only reported national total, not a sum of regional + national records.
fig, ax = plt.subplots(figsize=(9.4,5.7))
sns.lineplot(data=national, x='year', y='total_crime_incidents', marker='o', markersize=9,
             linewidth=2.4, color='#28649c', ax=ax)
for _,r in national.iterrows():
    ax.annotate(f"{int(r.total_crime_incidents):,}", (r.year,r.total_crime_incidents),
                xytext=(0,11), textcoords='offset points', ha='center', fontsize=9)
ax.set(title='Total Reported Crime Incidents in the Philippines (2020–2024)',
       xlabel='Year', ylabel='Reported crime incidents', xticks=national.year.tolist())
ax.set_ylim(350000, 415000)
fig.tight_layout();fig.savefig(OUT/'02_line_plot.png',dpi=220,bbox_inches='tight');plt.close(fig)

# 3. HEATMAP: regions by year, raw rates (not normalized).
rate=regional.pivot(index='region',columns='year',values='average_monthly_crime_rate').sort_index()
fig, ax = plt.subplots(figsize=(10.6,10))
sns.heatmap(rate, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=.4, linecolor='white',
            cbar_kws={'label':'Average monthly crime rate per 100,000'}, ax=ax)
ax.set(title='Average Monthly Crime Rate by Region and Year',xlabel='Year',ylabel='Region')
fig.tight_layout();fig.savefig(OUT/'03_heatmap.png',dpi=220,bbox_inches='tight');plt.close(fig)

# 4. CLUSTER MAP: selected per-year rates and efficiencies, column z-score scaling.
# 10 features per region. Ward hierarchical clustering with Euclidean distance.
rate_cols=rate.rename(columns=lambda y:f'Rate_{y}')
eff=regional.pivot(index='region',columns='year',values='crime_solution_efficiency_pct').sort_index()
eff_cols=eff.rename(columns=lambda y:f'Eff_{y}')
features=pd.concat([rate_cols,eff_cols],axis=1)
features=features[[f'Rate_{y}' for y in range(2020,2025)]+[f'Eff_{y}' for y in range(2020,2025)]]
z=(features-features.mean(axis=0))/features.std(axis=0,ddof=1)
assert z.notna().all().all(), 'Cannot cluster missing or constant features'
features.to_csv(BASE/'data/processed/cluster_features_raw.csv')
z.to_csv(BASE/'data/processed/cluster_features_zscores.csv')
g=sns.clustermap(z, method='ward', metric='euclidean', row_cluster=True,
                 col_cluster=False, cmap='vlag', center=0, linewidths=.35,
                 figsize=(13,10), dendrogram_ratio=(.17,.08),
                 cbar_pos=(.03,.82,.025,.13),
                 cbar_kws={'label':'Standardized z-score'})
g.ax_heatmap.set_xlabel('Annual crime-rate and solution-efficiency indicators')
g.ax_heatmap.set_ylabel('Region')
g.ax_heatmap.tick_params(axis='x',rotation=60,labelsize=8)
g.fig.suptitle('Regional Crime Indicator Profiles: Hierarchical Cluster Map', y=1.02, fontsize=14)
g.fig.savefig(OUT/'04_cluster_map.png',dpi=220,bbox_inches='tight');plt.close(g.fig)

# Document factual summary derived from CSV.
first=national.iloc[0];last=national.iloc[-1]
change=(last.total_crime_incidents/first.total_crime_incidents-1)*100
cor,pval=pearsonr(regional.average_monthly_crime_rate,regional.crime_solution_efficiency_pct)
summary=f"""INITIAL DESCRIPTIVE RESULTS — NOT CAUSAL FINDINGS
Source: supplied dataset mirrored from PSA OpenSTAT, Table 17.4 (PNP CIRAS), 2020–2024.
Geographic entries: 17 regions and 1 Philippines national total; 90 region-year rows.
National total incidents in 2020: {int(first.total_crime_incidents):,}.
National total incidents in 2024: {int(last.total_crime_incidents):,}.
Net change from 2020 to 2024: {change:+.2f}%.
Regional scatterplot includes {len(regional)} region-year observations; repeated regions across years.
Pooled Pearson r between rate and efficiency: {cor:.3f} (descriptive only; pooled observations are not independent).
Heatmap values are rates per 100,000 population; they are not incident counts.
Cluster map uses 10 annual features (five rates, five solution-efficiency percentages),
column-wise sample z-scores, Euclidean distance, and Ward linkage; it is NOT a geographic crime hotspot map.
Source availability and regional reporting definitions should be checked in the original PSA metadata before final interpretation.
"""
(BASE/'reports/initial_findings.txt').write_text(summary)
print(summary)
print('Saved 4 PNG visualizations to:',OUT)
