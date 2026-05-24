# Binder Deployment Notes

Purpose: record how the dashboard is expected to launch through BinderHub.

The repository is designed for repo2docker and BinderHub. The `.binder`
directory installs the package in editable mode and compiles the Python modules
as a quick build-time sanity check.

Preferred launch URL paths:

```text
urlpath=/panel/campaign_dashboard
urlpath=/panel/studies_dashboard
```

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
