# Dashboard Status

Purpose: summarize what the current Binder dashboard scaffold can do and what
still needs production artifact wiring.

## Ready Now

- Launches two Binder entrypoints: the campaign dashboard and the studies
  dashboard.
- Uses a public sample manifest with DataLoader, DDP, NCCL, GDS, HPL-MxP, and
  HPCG entries.
- Shows coverage cards, module/cluster filters, provenance links, public study
  links, and simple Plotly coverage charts.
- Lets a reader preview small public CSV and JSON artifacts on demand.
- Validates the manifest schema, dashboard imports, URL shape, and notebook
  execution in CI.

## Seed Manifest Limits

- The manifest is hand-written and intentionally small.
- HPL-MxP and HPCG entries are marked as planned until results-backed public
  study pages and artifacts are finalized.
- Large tarballs remain links only; the dashboard does not download or cache
  raw benchmark bundles.
- Numeric plots are generic until each module has a stable exported summary
  schema.

## Next Production Steps

- Generate the manifest from the public benchmark repository rather than
  editing it by hand.
- Add module-specific plot builders for the DataLoader/DDP handoff, NCCL/GDS
  throughput, HPL-MxP precision studies, and HPCG diagnostic rows.
- Add a small pinned cache only if BinderHub cannot reach the public OSN
  artifact URLs.
- Replace planned HPL-MxP and HPCG entries with results-backed entries after
  their public study pages and artifacts are complete.
