"""Panel entrypoint for the studies dashboard."""

from apps.studies.components import build_dashboard
from lib.manifest import load_dashboard_manifest, panel_query_params

load_result = load_dashboard_manifest(query_params=panel_query_params())
build_dashboard(load_result.manifest, load_result).servable(title="AICR Study Dashboard")
