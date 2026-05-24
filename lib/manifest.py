"""Manifest loading and validation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


DEFAULT_MANIFEST = Path("data/manifests/manifest.sample.json")
DEFAULT_SCHEMA = Path("data/schema/manifest.schema.json")


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON object from a repository-relative or absolute path."""
    resolved = Path(path)
    with resolved.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {resolved}")
    return value


def load_manifest(path: str | Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    """Load a dashboard manifest."""
    return load_json(path)


def load_schema(path: str | Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    """Load the manifest JSON schema."""
    return load_json(path)


def validate_manifest(
    manifest: dict[str, Any],
    schema: dict[str, Any] | None = None,
) -> None:
    """Validate a manifest and raise on schema errors."""
    validator = Draft202012Validator(schema or load_schema())
    validator.validate(manifest)


def entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Return manifest entries as a list."""
    values = manifest.get("artifacts", [])
    if not isinstance(values, list):
        raise ValueError("manifest.artifacts must be a list")
    return [entry for entry in values if isinstance(entry, dict)]


def sorted_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Return entries in stable dashboard order."""
    return sorted(
        entries(manifest),
        key=lambda item: (
            str(item.get("module", "")),
            str(item.get("cluster", "")),
            str(item.get("date", "")),
            str(item.get("title", "")),
        ),
    )


def unique_values(manifest: dict[str, Any], field: str) -> list[str]:
    """Return sorted non-empty unique values for a field."""
    values = {str(entry.get(field, "")) for entry in entries(manifest)}
    return sorted(value for value in values if value)


def count_by(manifest: dict[str, Any], field: str) -> dict[str, int]:
    """Count entries by a field."""
    counts: dict[str, int] = {}
    for entry in entries(manifest):
        value = str(entry.get(field, "unknown") or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))

