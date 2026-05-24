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

