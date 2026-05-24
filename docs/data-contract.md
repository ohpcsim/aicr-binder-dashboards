# Dashboard Data Contract

Purpose: define the minimum public artifact metadata consumed by the Binder
dashboards.

The dashboard manifest is a small JSON file with a `schema_version`,
`generated_at`, and an `artifacts` array. Each artifact entry describes one
public CSV, JSON, Markdown page, tarball, or checksum that supports a benchmark
campaign or study view.

Dashboards load manifests in this order:

1. `manifest_url` query parameter.
2. `AICR_DASHBOARD_MANIFEST_URL`.
3. Public OSN `latest` manifest.
4. Bundled generated manifest.

Every dashboard shows the active manifest source and `generated_at` value.

Required fields:

- `id`: stable dashboard identifier.
- `title`: short user-facing artifact name.
- `module`: benchmark module, such as `dataloader`, `ddp`, `hpcg`, `nccl`,
  or `gds`.
- `study`: study or campaign branch name.
- `cluster`: `b200`, `rtxpro6000`, `mixed`, or another explicit scope.
- `date`: artifact date.
- `role`: `campaign`, `canonical`, `supporting`, `appendix`, `diagnostic`,
  or `planned`.
- `evidence_type`: high-level evidence category.
- `artifact_type`: artifact role, such as `summary-csv` or `provenance-json`.
- `format`: `csv`, `json`, `markdown`, `tar.gz`, `sha256`, or `other`.
- `url`: public artifact URL.
- `public_page`: public GitHub study or module page.

Optional fields such as `provenance_url`, `checksum_url`, `bundle_url`,
`local_path`, `source_page`, `source_table`, `source_kind`, `commit`, `notes`,
and `metrics` provide dashboard context without forcing every module to share
the same numeric schema.

`local_path` is used only for small CSV tables bundled in this dashboard repo.
Those tables are extracted from public Markdown study pages for plotting; the
linked public page and OSN artifacts remain the authoritative evidence.
