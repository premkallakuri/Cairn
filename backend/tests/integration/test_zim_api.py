import pytest

pytestmark = [pytest.mark.integration, pytest.mark.zim]


def test_zim_list_and_wikipedia_state_endpoints(client) -> None:
    state_response = client.get("/api/zim/wikipedia")
    list_response = client.get("/api/zim/list")

    assert state_response.status_code == 200
    assert list_response.status_code == 200
    assert any(option["id"] == "top-mini" for option in state_response.json()["options"])
    assert list_response.json()["files"] == []


def test_select_wikipedia_endpoint_seeds_demo_file_and_lists_it(client) -> None:
    select_response = client.post("/api/zim/wikipedia/select", json={"optionId": "top-mini"})
    list_response = client.get("/api/zim/list")

    assert select_response.status_code == 200
    assert select_response.json()["success"] is True
    assert list_response.status_code == 200
    assert any(
        file["name"] == "wikipedia_en_100_mini_2025-06.zim"
        for file in list_response.json()["files"]
    )


def test_download_remote_and_category_tier_queue_download_jobs(client) -> None:
    remote_response = client.post(
        "/api/zim/download-remote",
        json={"url": "https://download.kiwix.org/zim/custom.zim"},
    )
    tier_response = client.post(
        "/api/zim/download-category-tier",
        json={"categorySlug": "medicine", "tierSlug": "medicine-essential"},
    )
    jobs_response = client.get("/api/downloads/jobs/zim")

    assert remote_response.status_code == 200
    assert tier_response.status_code == 200
    assert jobs_response.status_code == 200
    assert remote_response.json()["filename"] == "custom.zim"
    assert tier_response.json()["categorySlug"] == "medicine"
    assert len(jobs_response.json()) == 5
