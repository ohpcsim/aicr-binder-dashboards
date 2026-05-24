from pathlib import Path

from lib.manifest import entries, load_manifest, load_schema, validate_manifest


def test_sample_manifest_validates():
    manifest = load_manifest(Path("data/manifests/manifest.sample.json"))
    validate_manifest(manifest, load_schema(Path("data/schema/manifest.schema.json")))
    assert len(entries(manifest)) >= 5


def test_sample_manifest_has_expected_modules():
    manifest = load_manifest()
    modules = {entry["module"] for entry in entries(manifest)}
    assert {"dataloader", "ddp", "gds", "hpcg", "hpl-mxp", "nccl"}.issubset(modules)
