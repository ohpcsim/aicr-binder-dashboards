"""Provenance formatting helpers."""

from __future__ import annotations

from typing import Any


def public_link(entry: dict[str, Any]) -> str:
    """Return a Markdown link to the public study page when available."""
    page = str(entry.get("public_page", "") or "")
    title = str(entry.get("title", "study") or "study")
    return f"[{title}]({page})" if page else title


def artifact_link(entry: dict[str, Any]) -> str:
    """Return a Markdown link to the artifact."""
    url = str(entry.get("url", "") or "")
    label = str(entry.get("artifact_type", "artifact") or "artifact")
    return f"[{label}]({url})" if url else label


def provenance_markdown(entry: dict[str, Any]) -> str:
    """Format key provenance fields for display."""
    parts = [
        f"**Module:** `{entry.get('module', 'unknown')}`",
        f"**Study:** `{entry.get('study', 'unknown')}`",
        f"**Cluster:** `{entry.get('cluster', 'mixed')}`",
        f"**Date:** `{entry.get('date', 'unknown')}`",
        f"**Evidence:** `{entry.get('evidence_type', 'unknown')}`",
    ]
    if entry.get("commit"):
        parts.append(f"**Commit:** `{entry['commit']}`")
    if entry.get("public_page"):
        parts.append(f"**Page:** {public_link(entry)}")
    if entry.get("url"):
        parts.append(f"**Artifact:** {artifact_link(entry)}")
    return "  \n".join(parts)

