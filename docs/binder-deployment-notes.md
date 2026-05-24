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

If BinderHub egress to OSN is unavailable, the dashboard still renders the
manifest, public study links, and provenance links. Add cache-backed examples
only after the public URL behavior is verified.
