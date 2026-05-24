from urllib.parse import urlparse

from lib.manifest import entries, load_manifest


def test_manifest_urls_are_public_http_urls():
    manifest = load_manifest()
    for entry in entries(manifest):
        for field in ("url", "public_page"):
            parsed = urlparse(entry[field])
            assert parsed.scheme in {"http", "https"}
            assert parsed.netloc


def test_no_manifest_entry_points_to_local_work_tree():
    manifest = load_manifest()
    for entry in entries(manifest):
        assert "/Users/" not in entry["url"]
        assert "/work/" not in entry["url"]

