from pathlib import Path

import httpx
import pytest

from app.modules.zim.schemas import WikipediaSelectionRequest
from app.modules.zim.service import KiwixCatalogClient, ZimService

pytestmark = [pytest.mark.unit, pytest.mark.zim]


def test_delete_rejects_path_traversal() -> None:
    service = ZimService()

    with pytest.raises(ValueError, match="Invalid filename"):
        service.delete("../outside.zim")


def test_select_wikipedia_top_mini_seeds_bundled_file_and_replaces_old_copy(tmp_path: Path) -> None:
    service = ZimService()
    zim_dir = service.get_zim_storage_path()
    zim_dir.mkdir(parents=True, exist_ok=True)
    old_file = zim_dir / "wikipedia_en_old_nopic.zim"
    old_file.write_bytes(b"old")

    response = service.select_wikipedia(WikipediaSelectionRequest(optionId="top-mini"))

    assert response.success is True
    assert response.message == "Bundled demo Wikipedia is ready"
    assert not old_file.exists()

    state = service.get_wikipedia_state()
    assert state.currentSelection is not None
    assert state.currentSelection.optionId == "top-mini"
    assert state.currentSelection.status == "installed"
    assert state.currentSelection.filename == "wikipedia_en_100_mini_2025-06.zim"
    assert (zim_dir / "wikipedia_en_100_mini_2025-06.zim").read_bytes() == b"atlas-haven-demo-zim"


def test_remote_catalog_client_parses_entries_and_filters_existing_files(tmp_path: Path) -> None:
    xml_payload = """
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
      <opensearch:totalResults>2</opensearch:totalResults>
      <entry>
        <id>alpha</id>
        <title>Alpha Library</title>
        <updated>2026-03-20T00:00:00Z</updated>
        <summary>Alpha summary</summary>
        <author><name>Atlas</name></author>
        <link
          rel="enclosure"
          type="application/x-zim"
          href="https://download.kiwix.org/zim/alpha.zim.meta4"
          length="10"
        />
      </entry>
      <entry>
        <id>beta</id>
        <title>Beta Library</title>
        <updated>2026-03-20T00:00:00Z</updated>
        <summary>Beta summary</summary>
        <author><name>Atlas</name></author>
        <link
          rel="enclosure"
          type="application/x-zim"
          href="https://download.kiwix.org/zim/beta.zim.meta4"
          length="20"
        />
      </entry>
    </feed>
    """

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=xml_payload)

    service = ZimService(
        catalog_client=KiwixCatalogClient(
            client_factory=lambda: httpx.Client(transport=httpx.MockTransport(handler))
        )
    )
    local_file = service.get_zim_storage_path() / "alpha.zim"
    local_file.parent.mkdir(parents=True, exist_ok=True)
    local_file.write_bytes(b"existing")

    payload = service.list_remote(start=0, count=12)

    assert payload.total_count == 2
    assert len(payload.items) == 1
    assert payload.items[0].id == "beta"
    assert payload.items[0].file_name == "beta.zim"


def test_installed_resource_versions_and_wikipedia_update_state() -> None:
    service = ZimService()
    zim_dir = service.get_zim_storage_path()
    zim_dir.mkdir(parents=True, exist_ok=True)
    (zim_dir / "wikipedia_en_top_mini_2025-06.zim").write_bytes(b"seed")

    service.select_wikipedia(WikipediaSelectionRequest(optionId="top-mini"))

    versions = service.get_installed_resource_versions()
    wikipedia_update_state = service.get_wikipedia_update_state()

    assert versions["wikipedia_en_100_mini"] == "2025-06"
    assert wikipedia_update_state.needs_update is True
    assert wikipedia_update_state.installed_version == "2025-06"
    assert wikipedia_update_state.latest_version == "2025-12"
