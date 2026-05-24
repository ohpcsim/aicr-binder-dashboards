"""Panel entrypoint for the studies dashboard."""

from apps.studies.components import build_dashboard
from lib.manifest import load_manifest, validate_manifest

manifest = load_manifest("data/manifests/manifest.sample.json")
validate_manifest(manifest)
build_dashboard(manifest).servable(title="AICR Study Dashboard")
