# Philippine Crime Statistics — Web Dashboard

Public static React/Vite dashboard for ITD112 Group 5 (2020–2024). Includes all eight existing R and Python PNG charts, full regional table, year selector, static source notes, and CSV export.

## Install and run locally

From `ITD112_Crime_Project/dashboard`:

```bash
npm install
npm run dev
```

Open the local URL shown by Vite (typically http://localhost:5173/).

## Build

```bash
npm run build
```

The generated `dist/` folder is a self-contained static website.

## Deploy option A — Netlify Drop (fastest, no GitHub needed)

1. Run `npm run build`.
2. Visit https://app.netlify.com/drop and sign in if requested.
3. Drag the **dashboard/dist** folder to the page.
4. Netlify provides a public URL to share with classmates.

## Deploy option B — Vercel with GitHub (automatic future updates)

1. Upload the **dashboard** folder as the root of a GitHub repository (or set the Vercel Root Directory to `dashboard` if uploading the entire project).
2. Visit https://vercel.com/new and import the GitHub repository.
3. Framework: **Vite**. Build command: `npm run build`. Output directory: `dist`.
4. Deploy and share the generated URL.

No API, database, secret keys, or runtime R/Python server are needed. The chart files are static images created by the existing scripts. To update charts after rerunning R/Python analysis, replace the PNGs in `dashboard/public/charts/`, rebuild, and redeploy.

## Source and limitations

Official PSA OpenSTAT Table 17.4 sourced via third-party mirror. Data derived from PNP-CIRAS. 17 regions, 2020–2024. National total kept separately. Correlations are descriptive and clusters are *statistical*, not geographical hotspots. Dataset is versioned as supplied.
