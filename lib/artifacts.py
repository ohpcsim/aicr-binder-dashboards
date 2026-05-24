"""Helpers for local generated tables and small public artifact previews."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from pandas.api.types import is_numeric_dtype

from lib.manifest import REPO_ROOT, entries
from lib.osn import read_csv_url


def coerce_numeric_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with numeric-looking object columns converted."""
    converted = frame.copy()
    skip = {
        "backend",
        "candidate",
        "cluster",
        "dashboard_cluster",
        "dashboard_role",
        "dashboard_study",
        "dashboard_title",
        "evidence",
        "grid",
        "input",
        "job_ids",
        "mode",
        "node",
        "node_group",
        "notes",
        "outcome",
        "platform",
        "profile",
        "reading",
        "result_page",
        "run",
        "sloppy_type",
        "status",
        "study",
        "type",
        "view",
    }
    for column in converted.columns:
        if is_numeric_dtype(converted[column]) or column in skip:
            continue
        cleaned = (
            converted[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.extract(r"([-+]?[0-9]*\.?[0-9]+)", expand=False)
        )
        numeric = pd.to_numeric(cleaned, errors="coerce")
        if numeric.notna().sum() > 0:
            converted[column] = numeric
    return converted


def local_path(entry: dict[str, Any]) -> Path | None:
    """Return an existing local path for a manifest entry when bundled."""
    value = str(entry.get("local_path", "") or "")
    if not value:
        return None
    path = REPO_ROOT / value
    return path if path.exists() else None


def read_entry_csv(entry: dict[str, Any]) -> pd.DataFrame:
    """Read a manifest CSV entry from local generated data or a public URL."""
    path = local_path(entry)
    if path is not None:
        return coerce_numeric_columns(pd.read_csv(path))
    return coerce_numeric_columns(read_csv_url(str(entry["url"])))


def module_local_csv_frames(manifest: dict[str, Any], module: str) -> list[pd.DataFrame]:
    """Load bundled generated CSV frames for one module."""
    frames: list[pd.DataFrame] = []
    for entry in entries(manifest):
        if entry.get("module") != module:
            continue
        if entry.get("format") != "csv" or not entry.get("local_path"):
            continue
        path = local_path(entry)
        if path is None:
            continue
        frame = coerce_numeric_columns(pd.read_csv(path))
        frame["dashboard_title"] = entry.get("title", "")
        frame["dashboard_study"] = entry.get("study", "")
        frame["dashboard_cluster"] = entry.get("cluster", "")
        frame["dashboard_role"] = entry.get("role", "")
        frames.append(frame)
    return frames


def concat_module_frames(manifest: dict[str, Any], module: str) -> pd.DataFrame:
    """Concatenate bundled generated CSV frames for one module."""
    frames = module_local_csv_frames(manifest, module)
    if not frames:
        return pd.DataFrame()
    return coerce_numeric_columns(pd.concat(frames, ignore_index=True, sort=False))
