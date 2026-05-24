"""Plot helpers shared by the Binder dashboards."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px

from lib.manifest import count_by, entries


def manifest_frame(manifest: dict[str, Any]) -> pd.DataFrame:
    """Return a dashboard-friendly manifest table."""
    frame = pd.DataFrame(entries(manifest))
    if frame.empty:
        return pd.DataFrame(
            columns=[
                "title",
                "module",
                "study",
                "cluster",
                "date",
                "evidence_type",
                "artifact_type",
                "format",
                "url",
                "public_page",
            ]
        )
    return frame


def count_chart(manifest: dict[str, Any], field: str, title: str):
    """Build a Plotly count chart from manifest entries."""
    counts = count_by(manifest, field)
    frame = pd.DataFrame({"value": list(counts), "count": list(counts.values())})
    if frame.empty:
        frame = pd.DataFrame({"value": ["none"], "count": [0]})
    return px.bar(frame, x="value", y="count", title=title)


def evidence_scatter(manifest: dict[str, Any]):
    """Build a simple artifact coverage scatter."""
    frame = manifest_frame(manifest)
    if frame.empty:
        frame = pd.DataFrame(
            {"module": ["none"], "date": ["none"], "cluster": ["none"], "title": ["none"]}
        )
    return px.scatter(
        frame,
        x="date",
        y="module",
        color="cluster",
        hover_name="title",
        title="Artifact Coverage By Module And Date",
    )


def numeric_preview_chart(frame: pd.DataFrame, title: str = "Numeric Preview"):
    """Build a small line chart for the first numeric columns in a CSV artifact."""
    numeric = frame.select_dtypes(include="number")
    if numeric.empty:
        return None
    limited = numeric.iloc[:100, :4].reset_index(names="row")
    melted = limited.melt(id_vars="row", var_name="metric", value_name="value")
    return px.line(
        melted,
        x="row",
        y="value",
        color="metric",
        title=title,
        markers=True,
    )
