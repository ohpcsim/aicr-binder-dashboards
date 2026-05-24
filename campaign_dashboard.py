"""Panel entrypoint for the campaign dashboard."""

from apps.campaign.components import build_dashboard
from lib.manifest import load_dashboard_manifest, panel_query_params

load_result = load_dashboard_manifest(query_params=panel_query_params())
build_dashboard(load_result.manifest, load_result).servable(title="AICR Campaign Dashboard")
