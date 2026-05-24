"""Study-level Panel dashboard components."""

from __future__ import annotations

from typing import Any

import pandas as pd
import panel as pn

from lib.manifest import entries, unique_values
from lib.osn import read_csv_url, read_json_url
from lib.plots import count_chart, manifest_frame
from lib.provenance import provenance_markdown


def _entry_options(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    options: dict[str, dict[str, Any]] = {}
    for entry in entries(manifest):
        label = f"{entry.get('module', 'module')} / {entry.get('title', 'artifact')}"
        options[label] = entry
    return dict(sorted(options.items()))


def _filter_frame(frame: pd.DataFrame, module: str, evidence_type: str) -> pd.DataFrame:
    filtered = frame
    if module != "All":
        filtered = filtered[filtered["module"] == module]
    if evidence_type != "All":
        filtered = filtered[filtered["evidence_type"] == evidence_type]
    return filtered


def _json_preview(value: Any) -> pd.DataFrame:
    if isinstance(value, dict):
        rows = [{"key": key, "value": repr(val)[:240]} for key, val in value.items()]
        return pd.DataFrame(rows)
    if isinstance(value, list):
        rows = [{"index": idx, "value": repr(val)[:240]} for idx, val in enumerate(value[:100])]
        return pd.DataFrame(rows)
    return pd.DataFrame([{"value": repr(value)[:240]}])


def _numeric_profile(frame: pd.DataFrame) -> pd.DataFrame:
    numeric = frame.select_dtypes(include="number")
    if numeric.empty:
        return pd.DataFrame()
    profile = numeric.agg(["count", "mean", "min", "max"]).transpose().reset_index()
    return profile.rename(columns={"index": "metric"})


def build_dashboard(manifest: dict[str, Any]) -> pn.Column:
    """Build the study dashboard."""
    pn.extension("tabulator", "plotly")
    frame = manifest_frame(manifest)
    modules = ["All"] + unique_values(manifest, "module")
    evidence_types = ["All"] + unique_values(manifest, "evidence_type")
    module_select = pn.widgets.Select(label="Module", options=modules, value="All")
    evidence_select = pn.widgets.Select(
        label="Evidence Type", options=evidence_types, value="All"
    )
    entry_options = _entry_options(manifest)
    entry_select = pn.widgets.Select(
        label="Artifact",
        options=entry_options,
        value=next(iter(entry_options.values()), {}),
        sizing_mode="stretch_width",
    )
    load_button = pn.widgets.Button(label="Load selected artifact preview", color="primary")

    @pn.depends(module_select, evidence_select)
    def table(module: str, evidence_type: str):
        visible = _filter_frame(frame, module, evidence_type)
        columns = [
            col
            for col in [
                "title",
                "module",
                "study",
                "cluster",
                "date",
                "role",
                "evidence_type",
                "artifact_type",
                "format",
                "public_page",
                "url",
            ]
            if col in visible.columns
        ]
        return pn.widgets.Tabulator(
            visible[columns],
            pagination="remote",
            page_size=12,
            sizing_mode="stretch_width",
            disabled=True,
        )

    @pn.depends(entry_select)
    def provenance(entry: dict[str, Any]):
        if not entry:
            return pn.pane.Markdown("No artifact selected.")
        return pn.pane.Markdown(provenance_markdown(entry), sizing_mode="stretch_width")

    @pn.depends(load_button.param.clicks, entry_select)
    def artifact_preview(clicks: int, entry: dict[str, Any]):
        if not clicks:
            return pn.pane.Markdown(
                "Click **Load selected artifact preview** to fetch a small public CSV/JSON artifact."
            )
        if not entry:
            return pn.pane.Markdown("No artifact selected.")
        artifact_format = entry.get("format")
        try:
            if artifact_format == "csv":
                frame = read_csv_url(str(entry["url"]))
                preview = pn.widgets.Tabulator(
                    frame.head(100),
                    pagination="remote",
                    page_size=10,
                    sizing_mode="stretch_width",
                    disabled=True,
                )
                profile_frame = _numeric_profile(frame)
                if profile_frame.empty:
                    return pn.Column("### Artifact Preview", preview)
                profile = pn.widgets.Tabulator(
                    profile_frame,
                    pagination="remote",
                    page_size=10,
                    sizing_mode="stretch_width",
                    disabled=True,
                )
                return pn.Column("### Artifact Preview", preview, "### Numeric Profile", profile)
            if artifact_format == "json":
                value = read_json_url(str(entry["url"]))
                frame = _json_preview(value)
                return pn.Column(
                    "### JSON Preview",
                    pn.widgets.Tabulator(
                        frame,
                        pagination="remote",
                        page_size=10,
                        sizing_mode="stretch_width",
                        disabled=True,
                    ),
                )
        except Exception as exc:  # pragma: no cover - depends on remote service state.
            return pn.pane.Alert(
                f"Could not load artifact preview: {exc}", alert_type="warning"
            )
        return pn.pane.Markdown(
            "Preview is available for CSV and JSON artifacts. Use the artifact link for this entry."
        )

    headline = pn.pane.Markdown(
        "## AICR Module Study Results\n\n"
        "Study-level artifact links and provenance for published benchmark modules.",
        sizing_mode="stretch_width",
    )
    controls = pn.Row(module_select, evidence_select, sizing_mode="stretch_width")
    chart = pn.pane.Plotly(count_chart(manifest, "evidence_type", "Artifacts By Evidence Type"))
    return pn.Column(
        headline,
        controls,
        chart,
        table,
        "### Selected Artifact",
        entry_select,
        provenance,
        load_button,
        artifact_preview,
        sizing_mode="stretch_width",
    )
