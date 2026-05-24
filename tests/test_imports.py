def test_core_imports():
    import lib.manifest
    import lib.osn
    import lib.plots
    import lib.provenance

    assert lib.manifest.DEFAULT_MANIFEST


def test_dashboard_components_import():
    import pytest

    pytest.importorskip("panel")
    import apps.campaign.components
    import apps.studies.components

    assert apps.campaign.components.build_dashboard
    assert apps.studies.components.build_dashboard


def test_dashboard_components_build():
    import pytest

    pytest.importorskip("panel")
    from apps.campaign.components import build_dashboard as build_campaign
    from apps.studies.components import (
        build_dashboard as build_studies,
        build_module_dashboard,
    )
    from lib.manifest import load_manifest, validate_manifest

    manifest = load_manifest()
    validate_manifest(manifest)
    campaign = build_campaign(manifest)
    studies = build_studies(manifest)
    dataloader = build_module_dashboard(manifest, "dataloader")

    assert len(campaign) >= 4
    assert len(studies) >= 7
    assert len(dataloader) >= 7
