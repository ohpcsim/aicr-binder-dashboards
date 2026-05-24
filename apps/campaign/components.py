"""Campaign-level Panel dashboard components."""

from __future__ import annotations

from typing import Any

import pandas as pd
import panel as pn

from lib.manifest import unique_values
from lib.plots import count_chart, evidence_scatter, manifest_frame


def _summary_cards(frame: pd.DataFrame) -> pn.Row:
    """Return compact campaign coverage cards."""
    artifact_count = len(frame)
    module_count = frame["module"].nunique() if "module" in frame else 0
    cluster_count = frame["cluster"].nunique() if "cluster" in frame else 0
    csv_json_count = (
        frame["format"].isin(["csv", "json"]).sum() if "format" in frame else 0
    )
    cards = [
        ("Artifacts", artifact_count),
        ("Modules", module_count),
        ("Clusters", cluster_count),
        ("Previewable CSV/JSON", csv_json_count),
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


def _filter_frame(frame: pd.DataFrame, module: str, cluster: str) -> pd.DataFrame:
    filtered = frame
    if module != "All":
        filtered = filtered[filtered["module"] == module]
    if cluster != "All":
        filtered = filtered[filtered["cluster"] == cluster]
    return filtered


def build_dashboard(manifest: dict[str, Any]) -> pn.Column:
    """Build the campaign dashboard."""
    pn.extension("tabulator", "plotly")
    frame = manifest_frame(manifest)
    modules = ["All"] + unique_values(manifest, "module")
    clusters = ["All"] + unique_values(manifest, "cluster")
    module_select = pn.widgets.Select(label="Module", options=modules, value="All")
    cluster_select = pn.widgets.Select(label="Cluster", options=clusters, value="All")

    @pn.depends(module_select, cluster_select)
    def table(module: str, cluster: str):
        visible = _filter_frame(frame, module, cluster)
        columns = [
            col
            for col in [
                "title",
                "module",
                "study",
                "cluster",
                "date",
                "evidence_type",
                "artifact_type",
                "public_page",
                "url",
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
    controls = pn.Row(module_select, cluster_select, sizing_mode="stretch_width")
    charts = pn.Row(
        pn.pane.Plotly(count_chart(manifest, "module", "Artifacts By Module")),
        pn.pane.Plotly(evidence_scatter(manifest)),
        sizing_mode="stretch_width",
    )
    return pn.Column(
        headline,
        _summary_cards(frame),
        controls,
        charts,
        table,
        sizing_mode="stretch_width",
    )
