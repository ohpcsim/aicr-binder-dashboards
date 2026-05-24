"""Campaign-level Panel dashboard components."""

from __future__ import annotations

from typing import Any

import pandas as pd
import panel as pn

from lib.manifest import ManifestLoadResult, unique_values
from lib.plots import count_chart, evidence_scatter, manifest_frame, timeline_chart


def _source_banner(load_result: ManifestLoadResult | None, manifest: dict[str, Any]):
    """Return manifest source provenance for the dashboard."""
    generated_at = manifest.get("generated_at", "unknown")
    if load_result is None:
        return pn.pane.Markdown(
            f"**Manifest:** bundled or caller-provided  \n**Generated:** `{generated_at}`",
            sizing_mode="stretch_width",
        )
    warning = f"  \n**Fallback note:** {load_result.warning}" if load_result.warning else ""
    return pn.pane.Markdown(
        f"**Manifest source:** `{load_result.source_kind}`  \n"
        f"**Manifest:** {load_result.source}  \n"
        f"**Generated:** `{generated_at}`"
        f"{warning}",
        sizing_mode="stretch_width",
    )


def _summary_cards(frame: pd.DataFrame) -> pn.Row:
    """Return compact campaign coverage cards."""
    artifact_count = len(frame)
    module_count = frame["module"].nunique() if "module" in frame else 0
    cluster_count = frame["cluster"].nunique() if "cluster" in frame else 0
    csv_json_count = (
        frame["format"].isin(["csv", "json"]).sum() if "format" in frame else 0
    )
    result_backed = (
        (~frame["role"].isin(["planned", "diagnostic"])).sum() if "role" in frame else 0
    )
    planned = frame["role"].isin(["planned", "diagnostic"]).sum() if "role" in frame else 0
    cards = [
        ("Artifacts", artifact_count),
        ("Modules", module_count),
        ("Clusters", cluster_count),
        ("Previewable CSV/JSON", csv_json_count),
        ("Result-backed Entries", int(result_backed)),
        ("Planned/Diagnostic", int(planned)),
    ]
    return pn.Row(
        *[
            pn.pane.Markdown(
                f"### {value}\n{label}",
                sizing_mode="stretch_width",
            )
            for label, value in cards
        ],
        sizing_mode="stretch_width",
    )


def _filter_frame(
    frame: pd.DataFrame,
    module: str,
    cluster: str,
    role: str,
    evidence_type: str,
    artifact_format: str,
    date: str,
) -> pd.DataFrame:
    filtered = frame
    if module != "All":
        filtered = filtered[filtered["module"] == module]
    if cluster != "All":
        filtered = filtered[filtered["cluster"] == cluster]
    if role != "All":
        filtered = filtered[filtered["role"] == role]
    if evidence_type != "All":
        filtered = filtered[filtered["evidence_type"] == evidence_type]
    if artifact_format != "All":
        filtered = filtered[filtered["format"] == artifact_format]
    if date != "All":
        filtered = filtered[filtered["date"] == date]
    return filtered


def build_dashboard(
    manifest: dict[str, Any],
    load_result: ManifestLoadResult | None = None,
) -> pn.Column:
    """Build the campaign dashboard."""
    pn.extension("tabulator", "plotly")
    frame = manifest_frame(manifest)
    modules = ["All"] + unique_values(manifest, "module")
    clusters = ["All"] + unique_values(manifest, "cluster")
    roles = ["All"] + unique_values(manifest, "role")
    evidence_types = ["All"] + unique_values(manifest, "evidence_type")
    formats = ["All"] + unique_values(manifest, "format")
    dates = ["All"] + unique_values(manifest, "date")
    module_select = pn.widgets.Select(label="Module", options=modules, value="All")
    cluster_select = pn.widgets.Select(label="Cluster", options=clusters, value="All")
    role_select = pn.widgets.Select(label="Role", options=roles, value="All")
    evidence_select = pn.widgets.Select(
        label="Evidence Type", options=evidence_types, value="All"
    )
    format_select = pn.widgets.Select(label="Format", options=formats, value="All")
    date_select = pn.widgets.Select(label="Date", options=dates, value="All")

    @pn.depends(module_select, cluster_select, role_select, evidence_select, format_select, date_select)
    def table(
        module: str,
        cluster: str,
        role: str,
        evidence_type: str,
        artifact_format: str,
        date: str,
    ):
        visible = _filter_frame(
            frame, module, cluster, role, evidence_type, artifact_format, date
        )
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
                "provenance_url",
                "checksum_url",
            ]
            if col in visible.columns
        ]
        return pn.widgets.Tabulator(
            visible[columns],
            pagination="remote",
            page_size=10,
            sizing_mode="stretch_width",
            disabled=True,
        )

    headline = pn.pane.Markdown(
        "## AICR Cambridge Benchmark Campaign\n\n"
        "Public artifact coverage, provenance links, and study evidence across modules.",
        sizing_mode="stretch_width",
    )
    controls = pn.Column(
        pn.Row(module_select, cluster_select, role_select, sizing_mode="stretch_width"),
        pn.Row(evidence_select, format_select, date_select, sizing_mode="stretch_width"),
        sizing_mode="stretch_width",
    )
    charts_one = pn.Row(
        pn.pane.Plotly(count_chart(manifest, "module", "Artifacts By Module")),
        pn.pane.Plotly(evidence_scatter(manifest)),
        sizing_mode="stretch_width",
    )
    charts_two = pn.Row(
        pn.pane.Plotly(count_chart(manifest, "role", "Entries By Role")),
        pn.pane.Plotly(timeline_chart(manifest)),
        sizing_mode="stretch_width",
    )
    return pn.Column(
        headline,
        _source_banner(load_result, manifest),
        _summary_cards(frame),
        controls,
        charts_one,
        charts_two,
        "### Campaign Artifact Index",
        table,
        sizing_mode="stretch_width",
    )
