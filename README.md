# AICR Binder Dashboards

Purpose: provide Binder-ready dashboards for the public AICR Cambridge benchmark
campaign and module study results.

This repository contains two public Panel dashboard entrypoints:

- Campaign dashboard: high-level coverage and artifact navigation across the
  Cambridge benchmark campaign.
- Studies dashboard: module and study-level views for DataLoader, DDP, HPCG,
  HPL-MxP, NCCL, and GDS artifacts.

## Binder Launch Paths

Use these Binder URL paths after the image builds:

```text
urlpath=/panel/campaign_dashboard
urlpath=/panel/studies_dashboard
```

Direct launch links:

- [Campaign dashboard](https://mybinder.org/v2/gh/ohpcsim/aicr-binder-dashboards/main?urlpath=/panel/campaign_dashboard)
- [Studies dashboard](https://mybinder.org/v2/gh/ohpcsim/aicr-binder-dashboards/main?urlpath=/panel/studies_dashboard)

The dashboards try to read a public OSN `latest` manifest first, then fall back
to the bundled generated manifest at
`data/manifests/aicr-public.generated.json`. A user can override the manifest
without changing code by passing `manifest_url` in the URL query string or by
setting `AICR_DASHBOARD_MANIFEST_URL`.

Manifest entries point to public OSN or GitHub-hosted CSV/JSON artifacts,
public study pages, provenance JSON, checksums, and small generated CSV tables
extracted from public Markdown study pages. The studies dashboard can fetch
selected CSV/JSON entries on demand and show a table, numeric profile, and
quick chart. Large tarballs stay linked rather than downloaded.

## Local Checks

```bash
.venv/bin/python -m compileall lib apps tests scripts
pytest
```

Refresh the bundled manifest from the public benchmark repository with:

```bash
.venv/bin/python scripts/generate_manifest.py
```

## Documentation

- [Data contract](docs/data-contract.md)
- [Binder deployment notes](docs/binder-deployment-notes.md)
- [Current status](docs/status.md)

## Repository Layout

```text
.binder/                 Binder/repo2docker environment
campaign_dashboard.py    Panel campaign dashboard entrypoint
studies_dashboard.py     Panel studies dashboard entrypoint
apps/campaign/           Campaign dashboard notebook and components
apps/studies/            Study dashboard notebooks and components
data/generated/          Small CSVs extracted from public Markdown result tables
data/manifests/          Generated and sample dashboard manifests
data/schema/             Manifest JSON schema
lib/                     Shared loading, provenance, and plotting helpers
scripts/                 Manifest generation utilities
tests/                   Local validation
docs/                    Data contract and Binder notes
```

## License

License selection is pending project-owner review.
