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


def timeline_chart(manifest: dict[str, Any]):
    """Build a simple artifact timeline."""
    frame = manifest_frame(manifest)
    if frame.empty:
        frame = pd.DataFrame({"date": ["none"], "module": ["none"], "role": ["none"], "title": ["none"]})
    return px.scatter(
        frame,
        x="date",
        y="module",
        color="role" if "role" in frame else None,
        hover_name="title",
        title="Artifact Timeline",
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


def best_axis(frame: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first available axis column from candidates."""
    for candidate in candidates:
        if candidate in frame.columns:
            return candidate
    return None


def module_metric_chart(frame: pd.DataFrame, title: str):
    """Build a module metric chart from generated result-table data."""
    if frame.empty:
        return None
    numeric = frame.select_dtypes(include="number")
    if numeric.empty:
        return None
    x = best_axis(frame, ["nodes", "gpus", "gpu_count", "batch_size", "size", "date"])
    y = best_axis(
        frame,
        [
            "samples_per_second",
            "samples_s",
            "images_per_second",
            "images_s",
            "read_gib_s",
            "read_gib_per_second",
            "write_gib_s",
            "sequential_read_gib_s",
            "sequential_write_gib_s",
            "random_read_gib_s",
            "pflop_s",
            "olympic_pflop_s",
            "ar_olympic_avg",
            "rs_olympic_avg",
            "ag_olympic_avg",
            "a2a_olympic_avg",
            "busbw",
            "algbw",
            "throughput",
        ],
    )
    if y is None:
        y = numeric.columns[0]
    if x is None or x == y:
        limited = numeric.iloc[:, : min(4, len(numeric.columns))].reset_index(names="row")
        melted = limited.melt(id_vars="row", var_name="metric", value_name="value")
        return px.line(melted, x="row", y="value", color="metric", title=title, markers=True)
    frame = frame.dropna(subset=[x, y])
    if frame.empty:
        return None
    color = best_axis(frame, ["platform", "cluster", "dashboard_study", "type", "backend", "profile"])
    return px.scatter(
        frame,
        x=x,
        y=y,
        color=color,
        hover_name="dashboard_title" if "dashboard_title" in frame else None,
        title=title,
        trendline=None,
    )
