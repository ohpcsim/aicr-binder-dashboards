# Dashboard Status

Purpose: summarize what the current Binder dashboard scaffold can do and what
still needs production artifact wiring.

## Ready Now

- Launches two Binder entrypoints through `jupyter-panel-proxy`: the campaign
  dashboard and the studies dashboard.
- MyBinder build and launch were validated on 2026-05-24 from commit
  `5d0b442`, with both `/panel/campaign_dashboard` and
  `/panel/studies_dashboard` returning HTTP 200 inside the live Binder session.
- Tries a public OSN `latest` manifest first and falls back to the bundled
  generated manifest if the remote manifest is unavailable.
- Supports `manifest_url` query overrides and `AICR_DASHBOARD_MANIFEST_URL`
  environment overrides.
- Uses a generated manifest with DataLoader, DDP, NCCL, GDS, GPU Topology,
  Elbencho, HPL-MxP, and HPCG entries.
- Shows coverage cards, module/cluster/role/evidence/date filters,
  provenance links, public study links, and Plotly coverage charts.
- Provides module views for DataLoader, DDP, NCCL, GDS, HPL-MxP, and HPCG.
- Lets a reader preview small public CSV and JSON artifacts on demand.
- Includes small CSV tables extracted from public Markdown result tables for
  Binder-side plotting when no direct public CSV exists.
- Validates the manifest schema, dashboard imports, URL shape, and notebook
  execution in CI.

## Current Limits

- The OSN `latest` manifest is the intended remote source. Until it is
  published, dashboards use the bundled generated manifest.
- HPL-MxP FP8/FP4 rows remain pending revision and should not be interpreted as
  final dashboard evidence.
- HPCG entries remain planned until results-backed public study pages and
  artifacts are finalized.
- Large tarballs remain links only; the dashboard does not download or cache
  raw benchmark bundles.
- Some module plots are generated from public Markdown tables, so provenance
  links remain the authoritative source.

## Next Production Steps

- Publish the validated generated manifest to the OSN `dashboard-manifests`
  `latest` path.
- Add more module-specific plot builders as each module settles on stable
  exported summary schemas.
- Add a small pinned cache only if BinderHub cannot reach public OSN artifact
  URLs.
- Replace planned HPL-MxP and HPCG entries with results-backed entries after
  their public study pages and artifacts are complete.
