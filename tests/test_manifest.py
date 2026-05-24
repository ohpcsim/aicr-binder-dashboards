from pathlib import Path

from lib.manifest import (
    entries,
    load_dashboard_manifest,
    load_manifest,
    load_schema,
    resolve_manifest_sources,
    validate_manifest,
)


def test_sample_manifest_validates():
    manifest = load_manifest(Path("data/manifests/manifest.sample.json"))
    validate_manifest(manifest, load_schema(Path("data/schema/manifest.schema.json")))
    assert len(entries(manifest)) >= 5


def test_sample_manifest_has_expected_modules():
    manifest = load_manifest()
    modules = {entry["module"] for entry in entries(manifest)}
    assert {"dataloader", "ddp", "gds", "hpcg", "hpl-mxp", "nccl"}.issubset(modules)


def test_generated_manifest_validates():
    manifest = load_manifest(Path("data/manifests/aicr-public.generated.json"))
    validate_manifest(manifest, load_schema(Path("data/schema/manifest.schema.json")))
    assert len(entries(manifest)) >= 25


def test_manifest_source_order_prefers_query_and_env():
    sources = resolve_manifest_sources(
        query_params={"manifest_url": "https://example.org/query.json"},
        env={"AICR_DASHBOARD_MANIFEST_URL": "https://example.org/env.json"},
        default_remote_url="https://example.org/default.json",
    )
    assert sources[0] == ("query", "https://example.org/query.json")
    assert sources[1] == ("environment", "https://example.org/env.json")
    assert sources[2] == ("osn-latest", "https://example.org/default.json")
    assert sources[-1][0] == "bundled"


def test_manifest_loader_falls_back_to_bundled_when_remote_disabled(monkeypatch):
    monkeypatch.setenv("AICR_DASHBOARD_SKIP_DEFAULT_REMOTE", "1")
    result = load_dashboard_manifest(env=dict(AICR_DASHBOARD_SKIP_DEFAULT_REMOTE="1"))
    assert result.source_kind == "bundled"
    assert len(entries(result.manifest)) >= 25


def test_manifest_loader_uses_remote_override(monkeypatch):
    import lib.manifest as manifest_lib

    bundled = load_manifest(Path("data/manifests/manifest.sample.json"))

    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return bundled

    monkeypatch.setattr(manifest_lib.requests, "get", lambda *args, **kwargs: Response())
    result = load_dashboard_manifest(
        query_params={"manifest_url": "https://example.org/manifest.json"},
        env={"AICR_DASHBOARD_SKIP_DEFAULT_REMOTE": "1"},
    )
    assert result.source_kind == "query"
    assert result.source == "https://example.org/manifest.json"
