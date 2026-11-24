# ITD112 Group 5: ggplot2 versions of four charts.
# Run from project root: Rscript r/create_visualizations.R
# Install once: install.packages(c("readr", "dplyr", "tidyr", "ggplot2", "pheatmap"))
library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(pheatmap)

file <- 'data/processed/crime_analysis_ready.csv'
out <- 'visualizations/r'
dir.create(out, recursive=TRUE, showWarnings=FALSE)
df <- read_csv(file, show_col_types=FALSE)
regional <- df |> filter(region != 'Philippines')
national <- df |> filter(region == 'Philippines') |> arrange(year)
stopifnot(nrow(regional)==85, nrow(national)==5)

# 1. Scatterplot: matching axes and color by year.
p1 <- ggplot(regional, aes(x=average_monthly_crime_rate,
              y=crime_solution_efficiency_pct, color=factor(year))) +
      geom_point(size=2.7, alpha=.85) +
      labs(title='Regional Crime Rate vs. Crime Solution Efficiency (2020–2024)',
           x='Average monthly crime rate (per 100,000 population)',
           y='Crime solution efficiency (%)', color='Year') +
      theme_minimal(base_size=11)
ggsave(file.path(out,'01_scatterplot.png'), p1, width=10, height=6.5, dpi=220)

# 2. Line plot: national totals only.
p2 <- ggplot(national, aes(x=year, y=total_crime_incidents)) +
      geom_line(color='#28649c', linewidth=1) +
      geom_point(color='#28649c',size=3) +
      geom_text(aes(label=format(total_crime_incidents,big.mark=',',scientific=FALSE)),
                vjust=-.8, size=3.2) +
      scale_x_continuous(breaks=2020:2024) +
      coord_cartesian(ylim=c(350000,415000)) +
      labs(title='Total Reported Crime Incidents in the Philippines (2020–2024)',
           x='Year', y='Reported crime incidents') +
      theme_minimal(base_size=11)
ggsave(file.path(out,'02_line_plot.png'), p2, width=9.4, height=5.7, dpi=220)

# 3. Regional heatmap: raw unstandardized monthly crime rates.
p3 <- ggplot(regional, aes(x=factor(year), y=region,fill=average_monthly_crime_rate)) +
      geom_tile(color='white',linewidth=.3) +
      geom_text(aes(label=sprintf('%.1f',average_monthly_crime_rate)),size=2.6) +
      scale_fill_gradient(low='#fff3c9', high='#be3c2f',name='Rate per 100,000') +
      labs(title='Average Monthly Crime Rate by Region and Year',x='Year',y='Region') +
      theme_minimal(base_size=11)
ggsave(file.path(out,'03_heatmap.png'), p3, width=10.6, height=10,dpi=220)

# 4. Cluster map: use the SAME prepared z-score features as Python,
# Ward.D2 linkage + Euclidean distance. pheatmap is permitted as an R equivalent.
z <- read.csv('data/processed/cluster_features_zscores.csv',row.names=1,check.names=FALSE)
m <- as.matrix(z)
png(filename=file.path(out,'04_cluster_map.png'),width=2800,height=2200,res=220)
pheatmap(m, scale='none', cluster_rows=TRUE, cluster_cols=FALSE,
         clustering_method='ward.D2', clustering_distance_rows='euclidean',
         main='Regional Crime Indicator Profiles: Hierarchical Cluster Map',
         fontsize_row=9, fontsize_col=9, angle_col=45,
         border_color='white', color=colorRampPalette(c('#2166ac','white','#b2182b'))(101))
dev.off()
cat('Saved four R charts to',out,'\n')
