# Campaign Dashboard

Purpose: show campaign-level public artifact coverage and provenance links.

Launch path:

```text
urlpath=/panel/campaign_dashboard
```

The dashboard loads the active manifest from OSN, a URL override, an
environment override, or the bundled generated fallback. It summarizes entries
by module, cluster, date, role, evidence type, and artifact format. It includes
coverage cards, Plotly coverage charts, and a filterable artifact table with
provenance, checksum, public page, and artifact links. Use it as the front door
for campaign review.
