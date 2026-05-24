# AICR Binder Dashboards

Purpose: provide Binder-ready dashboards for the public AICR Cambridge benchmark
campaign and module study results.

This repository contains two public dashboard entrypoints:

- Campaign dashboard: high-level coverage and artifact navigation across the
  Cambridge benchmark campaign.
- Studies dashboard: module and study-level views for DataLoader, DDP, HPCG,
  HPL-MxP, NCCL, and GDS artifacts.

## Binder Launch Paths

Use these Binder URL paths after the image builds:

```text
urlpath=panel/apps/campaign/index
urlpath=panel/apps/studies/index
```

The dashboards read `data/manifests/manifest.sample.json` by default. Manifest
entries point to public OSN or GitHub-hosted CSV/JSON artifacts and public study
pages. The studies dashboard can fetch selected CSV/JSON entries on demand and
show a quick table/numeric profile. Cached data is not committed.

## Local Checks

```bash
python -m compileall lib apps tests
pytest
```

The first version uses a hand-written manifest and schema. A generator from the
public benchmark repository should be added after the schema and dashboards are
stable.

## Repository Layout

```text
.binder/                 Binder/repo2docker environment
apps/campaign/           Campaign dashboard notebook and components
apps/studies/            Study dashboard notebook and components
data/manifests/          Hand-written dashboard manifest
data/schema/             Manifest JSON schema
lib/                     Shared loading, provenance, and plotting helpers
tests/                   Local validation
docs/                    Data contract and Binder notes
```

## License

License selection is pending project-owner review.
