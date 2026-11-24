# GitHub + Vercel setup

## Overview
Repository contains project datasets, R and Python scripts, output images, and a React/Vite dashboard. Vercel publishes **only `dashboard/`**.

## Preview locally
```bash
cd dashboard
npm install
npm run dev
```
Open the URL shown by Vite. To verify the production build, run `npm run build`.

## Upload to GitHub
Create a **new empty** GitHub repository, e.g. `ITD112-Crime-Statistics`, without initializing README, license, or .gitignore. Run from **the outer `ITD112_Crime_Project` folder**:

```bash
git init
git add .
git commit -m "Initial crime statistics analysis and dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ITD112-Crime-Statistics.git
git push -u origin main
```

## Vercel
1. Log into https://vercel.com with GitHub.
2. Add New > Project and import the repository.
3. **Root Directory:** `dashboard` (critical).
4. **Framework:** Vite; **Build Command:** `npm run build`; **Output Directory:** `dist`.
5. Deploy and open the provided URL.
6. Future pushes to `main` automatically deploy updates to the published dashboard.

## Notes
- Do not commit `.venv`, `.RData`, `node_modules`, `.env` files, or credentials.
- Dashboard is a static presentation of the published data and chart images. Regenerate / copy updated images into `dashboard/public/charts/` and update `dashboard/src/data.json` when changing data.
- Publication to GitHub and Vercel is **not** performed by this package. You must connect your own accounts.
