#!/usr/bin/env python3
"""Generate the Binder dashboard manifest from public AICR study pages."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


BINDER_RAW_BASE = "https://raw.githubusercontent.com/ohpcsim/aicr-binder-dashboards/main"
PUBLIC_BLOB_BASE = "https://github.com/ohpcsim/aicr-public/blob/main/Cambridge/aicr-bench"
OSN_RE = re.compile(r"https://uma1\.osn\.mghpcc\.org/[^\s>)]+")
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_aicr_public_root() -> Path:
    candidate = repo_root().parent / "aicr-public" / "Cambridge" / "aicr-bench"
    if candidate.exists():
        return candidate
    return Path("/Users/chrissimmons/git/aicr-public/Cambridge/aicr-bench")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value.strip().lower()).strip("-")
    return cleaned or "entry"


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def module_from_path(path: Path) -> str:
    parts = path.parts
    if "modules" in parts:
        idx = parts.index("modules")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return "unknown"


def study_from_path(path: Path) -> str:
    if path.name == "studies.md":
        return "module-study-index"
    if path.name == "results-summary.md":
        return "results-summary"
    return path.stem


def infer_cluster(path: Path, text: str) -> str:
    blob = f"{path.as_posix()} {text[:4000]}".lower()
    has_b200 = "b200" in blob
    has_rtx = "rtx" in blob or "rtxpro6000" in blob or "rtx pro 6000" in blob
    if has_b200 and has_rtx:
        return "mixed"
    if has_b200:
        return "b200"
    if has_rtx:
        return "rtxpro6000"
    return "mixed"


def infer_role(path: Path, text: str) -> str:
    lower = text.lower()
    if "planned" in lower or "not collected" in lower or "no promoted" in lower:
        return "planned"
    if "diagnostic" in lower:
        return "diagnostic"
    if "appendix" in lower or "supporting" in lower:
        return "supporting"
    if path.name in {"studies.md", "results-summary.md"}:
        return "canonical"
    if any(token in path.stem for token in ("rdma", "fleet", "scale", "validation")):
        return "campaign"
    return "canonical"


def infer_evidence_type(module: str, study: str, text: str) -> str:
    blob = f"{module} {study} {text[:2000]}".lower()
    if module == "dataloader":
        if "dali" in blob or "backend" in blob:
            return "backend-crossover"
        return "input-throughput"
    if module == "ddp":
        return "training-throughput"
    if module == "nccl":
        return "communication-throughput"
    if module == "gds":
        return "storage-throughput"
    if module == "hpl-mxp":
        return "linear-algebra-throughput"
    if module == "hpcg":
        return "planned-diagnostic" if "planned" in blob else "hpcg-throughput"
    return "module-study"


def infer_artifact_type(url: str) -> tuple[str, str]:
    lower = url.lower()
    if lower.endswith(".csv"):
        return "summary-csv", "csv"
    if "provenance" in lower and lower.endswith(".json"):
        return "provenance-json", "json"
    if lower.endswith(".json"):
        return "summary-json", "json"
    if lower.endswith(".sha256") or lower.endswith("sha256sums"):
        return "checksum", "sha256"
    if lower.endswith(".tar.gz"):
        return "artifact-bundle", "tar.gz"
    if lower.endswith(".md"):
        return "study-page", "markdown"
    return "artifact", "other"


def find_date(text: str, urls: Iterable[str], fallback: str) -> str:
    for value in list(urls) + [text[:4000], fallback]:
        match = DATE_RE.search(value)
        if match:
            return match.group(1)
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def public_page_url(aicr_public_root: Path, path: Path) -> str:
    rel = path.relative_to(aicr_public_root).as_posix()
    return f"{PUBLIC_BLOB_BASE}/{rel}"


def clean_url(url: str) -> str:
    return url.rstrip(".,")


def osn_urls(text: str) -> list[str]:
    values = []
    for match in OSN_RE.finditer(text):
        url = clean_url(match.group(0))
        if url not in values:
            values.append(url)
    return values


def table_blocks(text: str) -> list[list[str]]:
    lines = text.splitlines()
    blocks: list[list[str]] = []
    index = 0
    while index < len(lines) - 1:
        line = lines[index]
        next_line = lines[index + 1]
        if line.strip().startswith("|") and re.match(r"^\s*\|?\s*:?-{3,}", next_line):
            block = [line, next_line]
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                block.append(lines[index])
                index += 1
            blocks.append(block)
        else:
            index += 1
    return blocks


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip().replace("<br>", " ") for cell in stripped.split("|")]


def header_slug(value: str) -> str:
    value = re.sub(r"`|\*|_", "", value)
    value = re.sub(r"\([^)]*\)", "", value)
    return slug(value).replace("-", "_")


def normalize_cell(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("`", "").replace("<", "").replace(">", "")
    return re.sub(r"\s+", " ", value).strip()


def result_table(headers: list[str], rows: list[list[str]]) -> bool:
    names = {header_slug(header) for header in headers}
    useful = {
        "platform",
        "cluster",
        "nodes",
        "gpus",
        "gpu",
        "n",
        "nb",
        "grid",
        "pflop_s",
        "pflip_s",
        "samples_s",
        "samples_per_second",
        "images_s",
        "read_gib_s",
        "busbw",
        "algbw",
        "throughput",
        "size",
        "backend",
        "mode",
    }
    if names & useful:
        return len(rows) > 0
    return False


def write_table_csv(
    output_dir: Path,
    module: str,
    study: str,
    table_index: int,
    block: list[str],
) -> Path | None:
    headers = split_table_row(block[0])
    rows = [split_table_row(line) for line in block[2:]]
    if not headers or not rows or not result_table(headers, rows):
        return None
    normalized_headers = [header_slug(header) for header in headers]
    if len(set(normalized_headers)) != len(normalized_headers):
        normalized_headers = [f"{name}_{idx}" for idx, name in enumerate(normalized_headers, 1)]
    path = output_dir / module / f"{study}-table-{table_index}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(normalized_headers)
        for row in rows:
            padded = row + [""] * max(0, len(headers) - len(row))
            writer.writerow([normalize_cell(cell) for cell in padded[: len(headers)]])
    return path


def companion_urls(urls: list[str]) -> dict[str, str]:
    companions: dict[str, str] = {}
    for url in urls:
        kind, _ = infer_artifact_type(url)
        if kind == "provenance-json":
            companions.setdefault("provenance_url", url)
        elif kind == "checksum":
            companions.setdefault("checksum_url", url)
        elif kind == "artifact-bundle":
            companions.setdefault("bundle_url", url)
    return companions


def page_entries(aicr_public_root: Path, path: Path, generated_dir: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    module = module_from_path(path)
    study = study_from_path(path)
    title = first_heading(text, study.replace("-", " ").title())
    page_url = public_page_url(aicr_public_root, path)
    urls = osn_urls(text)
    date = find_date(text, urls, path.name)
    role = infer_role(path, text)
    evidence_type = infer_evidence_type(module, study, text)
    cluster = infer_cluster(path, text)
    companions = companion_urls(urls)
    entries: list[dict[str, object]] = []

    for url_index, url in enumerate(urls, 1):
        artifact_type, artifact_format = infer_artifact_type(url)
        entries.append(
            {
                "id": slug(f"{module}-{study}-{date}-{artifact_type}-{url_index}"),
                "title": f"{title} {artifact_type.replace('-', ' ')}",
                "module": module,
                "study": study,
                "cluster": cluster,
                "date": date,
                "role": role,
                "evidence_type": evidence_type,
                "artifact_type": artifact_type,
                "format": artifact_format,
                "url": url,
                "public_page": page_url,
                **{key: value for key, value in companions.items() if value != url},
                "metrics": [],
            }
        )

    for table_index, block in enumerate(table_blocks(text), 1):
        table_path = write_table_csv(generated_dir, module, study, table_index, block)
        if table_path is None:
            continue
        rel = table_path.relative_to(repo_root()).as_posix()
        entries.append(
            {
                "id": slug(f"{module}-{study}-{date}-table-{table_index}"),
                "title": f"{title} table {table_index}",
                "module": module,
                "study": study,
                "cluster": cluster,
                "date": date,
                "role": role,
                "evidence_type": evidence_type,
                "artifact_type": "doc-extracted-table",
                "format": "csv",
                "url": f"{BINDER_RAW_BASE}/{rel}",
                "public_page": page_url,
                "local_path": rel,
                "source_page": page_url,
                "source_table": table_index,
                "source_kind": "public-doc-table",
                **companions,
                "notes": "Small CSV extracted from a public Markdown result table for Binder plotting.",
                "metrics": [],
            }
        )

    if not entries or path.name in {"studies.md", "results-summary.md"}:
        entries.append(
            {
                "id": slug(f"{module}-{study}-{date}-page"),
                "title": title,
                "module": module,
                "study": study,
                "cluster": cluster,
                "date": date,
                "role": role,
                "evidence_type": evidence_type,
                "artifact_type": "study-page",
                "format": "markdown",
                "url": page_url,
                "public_page": page_url,
                **companions,
                "metrics": [],
            }
        )

    return entries


def study_pages(aicr_public_root: Path) -> list[Path]:
    modules = aicr_public_root / "docs" / "modules"
    paths: list[Path] = []
    for pattern in ("*/studies.md", "*/results-summary.md", "*/studies/*.md"):
        paths.extend(modules.glob(pattern))
    return sorted(path for path in paths if path.is_file())


def generate(aicr_public_root: Path, output: Path, generated_dir: Path) -> dict[str, object]:
    if generated_dir.exists():
        for old in generated_dir.glob("**/*.csv"):
            old.unlink()
    artifacts: list[dict[str, object]] = []
    seen: set[str] = set()
    for path in study_pages(aicr_public_root):
        for entry in page_entries(aicr_public_root, path, generated_dir):
            original_id = str(entry["id"])
            entry_id = original_id
            suffix = 2
            while entry_id in seen:
                entry_id = f"{original_id}-{suffix}"
                suffix += 1
            entry["id"] = entry_id
            seen.add(entry_id)
            artifacts.append(entry)
    manifest = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "description": "Generated manifest for AICR Binder dashboards from public aicr-public study pages.",
        "artifacts": sorted(
            artifacts,
            key=lambda item: (
                str(item.get("module", "")),
                str(item.get("cluster", "")),
                str(item.get("date", "")),
                str(item.get("study", "")),
                str(item.get("artifact_type", "")),
            ),
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--aicr-public-root",
        type=Path,
        default=default_aicr_public_root(),
        help="Path to aicr-public/Cambridge/aicr-bench.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root() / "data" / "manifests" / "aicr-public.generated.json",
    )
    parser.add_argument(
        "--generated-dir",
        type=Path,
        default=repo_root() / "data" / "generated",
    )
    args = parser.parse_args()
    manifest = generate(args.aicr_public_root, args.output, args.generated_dir)
    print(f"Wrote {args.output} with {len(manifest['artifacts'])} artifact entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
