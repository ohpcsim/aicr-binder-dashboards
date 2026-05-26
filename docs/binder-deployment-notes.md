# Binder Deployment Notes

Purpose: record how the dashboard is expected to launch through BinderHub.

The repository is designed for repo2docker and BinderHub. The `.binder`
directory installs the package in editable mode and compiles the Python modules
as a quick build-time sanity check.

Preferred launch URL paths:

```text
urlpath=/panel/campaign_dashboard
urlpath=/panel/studies_dashboard
urlpath=/lab/tree/apps/story/dataloader_ddp_story.ipynb
```

The DataLoader teaching deck opens in JupyterLab and uses notebook slideshow
metadata for live presentation with `jupyterlab-rise`. It includes Plotly
dropdowns for the pipeline map, worker scan, backend crossover,
prepared-input economics, DDP validation, and synthetic-input ceiling views.
It also embeds pinned public DataLoader heatmaps, imbalance plots, candidate
frontiers, and scale plots as first-class story slides. It is intentionally
DataLoader-first; DDP appears only as training-validation handoff evidence.
For production teaching sessions, verify that Binder viewers can fetch the
pinned figure URLs from `ohpcsim/aicr-public`. If anonymous raw GitHub access is
not available in the deployment context, publish the same PNGs through an
approved static public asset host or use an authenticated BinderHub context.

The studies dashboard fetches small public CSV/JSON artifacts from OSN or
GitHub only when a viewer requests a preview. Large tarballs remain linked as
provenance and retrieval targets, not cached in git.

Manifest loading uses this order:

1. `manifest_url` query parameter.
2. `AICR_DASHBOARD_MANIFEST_URL`.
3. The public OSN `latest` manifest:
   `https://uma1.osn.mghpcc.org/csim-bmark/public-study-artifacts/aicr-public/dashboard-manifests/latest/aicr-public-dashboard-manifest.json`
4. Bundled `data/manifests/aicr-public.generated.json`.

If BinderHub egress to OSN is unavailable, the dashboard still renders with the
bundled generated manifest, public study links, provenance links, and small
generated CSV tables extracted from public Markdown result tables.

Use `manifest_url` to test a candidate manifest without changing the dashboard
code:

```text
https://mybinder.org/v2/gh/ohpcsim/aicr-binder-dashboards/main?urlpath=/panel/studies_dashboard&manifest_url=<encoded-manifest-url>
```
