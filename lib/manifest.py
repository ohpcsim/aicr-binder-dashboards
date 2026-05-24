"""Manifest loading and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import requests


DEFAULT_MANIFEST = Path("data/manifests/aicr-public.generated.json")
SAMPLE_MANIFEST = Path("data/manifests/manifest.sample.json")
DEFAULT_SCHEMA = Path("data/schema/manifest.schema.json")
DEFAULT_REMOTE_MANIFEST_URL = (
    "https://uma1.osn.mghpcc.org/csim-bmark/public-study-artifacts/"
    "aicr-public/dashboard-manifests/latest/aicr-public-dashboard-manifest.json"
)
REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ManifestLoadResult:
    """A dashboard manifest plus source metadata for user-facing provenance."""

    manifest: dict[str, Any]
    source: str
    source_kind: str
    warning: str = ""


def resolve_repo_path(path: str | Path) -> Path:
    """Resolve a path from the caller cwd or repository root."""
    resolved = Path(path)
    if resolved.is_absolute() or resolved.exists():
        return resolved
    return REPO_ROOT / resolved


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON object from a repository-relative or absolute path."""
    resolved = resolve_repo_path(path)
    with resolved.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {resolved}")
    return value


def load_manifest(path: str | Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    """Load a dashboard manifest."""
    return load_json(path)


def load_remote_manifest(url: str, timeout: int = 8) -> dict[str, Any]:
    """Load a manifest JSON object from a public HTTP(S) URL."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    value = response.json()
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object from {url}")
    return value


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


def manifest_url_from_query(query_params: dict[str, Any] | None = None) -> str:
    """Return a manifest_url override from Panel-style query params."""
    if not query_params:
        return ""
    value = query_params.get("manifest_url", "")
    if isinstance(value, (list, tuple)):
        value = value[0] if value else ""
    return str(value or "")


def panel_query_params() -> dict[str, Any]:
    """Best-effort access to Panel/Bokeh query parameters."""
    try:
        import panel as pn  # type: ignore

        location = getattr(pn.state, "location", None)
        if location is not None and getattr(location, "query_params", None):
            return dict(location.query_params)
        curdoc = getattr(pn.state, "curdoc", None)
        context = getattr(curdoc, "session_context", None)
        request = getattr(context, "request", None)
        arguments = getattr(request, "arguments", None)
        if arguments:
            decoded: dict[str, Any] = {}
            for key, values in arguments.items():
                if not values:
                    continue
                item = values[0]
                decoded[str(key)] = item.decode("utf-8") if isinstance(item, bytes) else item
            return decoded
    except Exception:
        return {}
    return {}


def resolve_manifest_sources(
    query_params: dict[str, Any] | None = None,
    env: dict[str, str] | None = None,
    default_remote_url: str = DEFAULT_REMOTE_MANIFEST_URL,
) -> list[tuple[str, str]]:
    """Return candidate manifest sources in dashboard precedence order."""
    environ = env if env is not None else os.environ
    candidates: list[tuple[str, str]] = []
    query_url = manifest_url_from_query(query_params)
    if query_url:
        candidates.append(("query", query_url))
    env_url = environ.get("AICR_DASHBOARD_MANIFEST_URL", "")
    if env_url:
        candidates.append(("environment", env_url))
    skip_default_remote = environ.get("AICR_DASHBOARD_SKIP_DEFAULT_REMOTE", "").lower()
    if default_remote_url and skip_default_remote not in {"1", "true", "yes"}:
        candidates.append(("osn-latest", default_remote_url))
    candidates.append(("bundled", str(DEFAULT_MANIFEST)))
    return candidates


def load_dashboard_manifest(
    query_params: dict[str, Any] | None = None,
    env: dict[str, str] | None = None,
    default_remote_url: str = DEFAULT_REMOTE_MANIFEST_URL,
    timeout: int = 8,
) -> ManifestLoadResult:
    """Load the dashboard manifest with remote sources and bundled fallback."""
    schema = load_schema()
    failures: list[str] = []
    for source_kind, source in resolve_manifest_sources(
        query_params=query_params,
        env=env,
        default_remote_url=default_remote_url,
    ):
        try:
            if source_kind == "bundled":
                manifest = load_manifest(source)
            else:
                manifest = load_remote_manifest(source, timeout=timeout)
            validate_manifest(manifest, schema)
            warning = "; ".join(failures)
            return ManifestLoadResult(
                manifest=manifest,
                source=source,
                source_kind=source_kind,
                warning=warning,
            )
        except Exception as exc:
            failures.append(f"{source_kind} manifest unavailable: {exc}")
    raise RuntimeError("no dashboard manifest source could be loaded")


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
