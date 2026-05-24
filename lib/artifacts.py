"""Helpers for local generated tables and small public artifact previews."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from lib.manifest import REPO_ROOT, entries
from lib.osn import read_csv_url


def coerce_numeric_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with numeric-looking object columns converted."""
    converted = frame.copy()
    for column in converted.columns:
        if converted[column].dtype != object:
            continue
        cleaned = (
            converted[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.extract(r"([-+]?[0-9]*\.?[0-9]+)", expand=False)
        )
        numeric = pd.to_numeric(cleaned, errors="coerce")
        if numeric.notna().sum() >= max(1, len(converted) // 3):
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
    return pd.concat(frames, ignore_index=True, sort=False)
