import pytest

pytestmark = [pytest.mark.integration, pytest.mark.easy_setup]


def test_easy_setup_uses_bundled_collection_data(client) -> None:
    response = client.get("/api/easy-setup/curated-categories")

    assert response.status_code == 200
    payload = response.json()
    assert any(category["slug"] == "medicine" for category in payload)


def test_easy_setup_bootstrap_exposes_default_draft_and_options(client) -> None:
    response = client.get("/api/easy-setup/bootstrap")

    assert response.status_code == 200
    payload = response.json()
    assert payload["draft"]["currentStep"] == 1
    assert payload["draft"]["selectedWikipediaOptionId"] == "none"
    assert any(option["id"] == "information" for option in payload["capabilities"])
    assert any(option["id"] == "notes" for option in payload["additionalTools"])
    assert any(collection["slug"] == "pacific" for collection in payload["mapCollections"])
    assert any(model["id"] == "deepseek-r1:1.5b" for model in payload["aiModels"])
    assert any(option["id"] == "top-mini" for option in payload["wikipediaOptions"])


def test_easy_setup_draft_can_be_saved_and_reloaded(client) -> None:
    draft = {
        "currentStep": 3,
        "selectedCapabilityIds": ["information", "ai"],
        "selectedMapCollectionSlugs": ["pacific"],
        "selectedCategoryTierSlugs": {"medicine": "medicine-essential"},
        "selectedAiModelIds": ["llama3.2:1b-text-q2_K"],
        "selectedWikipediaOptionId": "top-mini",
    }

    save_response = client.put("/api/easy-setup/draft", json=draft)
    reload_response = client.get("/api/easy-setup/draft")

    assert save_response.status_code == 200
    assert reload_response.status_code == 200
    assert reload_response.json() == draft


def test_easy_setup_plan_endpoint_expands_services_and_storage(client) -> None:
    response = client.post(
        "/api/easy-setup/plan",
        json={
            "currentStep": 4,
            "selectedCapabilityIds": ["ai", "datatools"],
            "selectedMapCollectionSlugs": ["pacific"],
            "selectedCategoryTierSlugs": {"medicine": "medicine-essential"},
            "selectedAiModelIds": ["llama3.2:1b-text-q2_K"],
            "selectedWikipediaOptionId": "top-mini",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert [service["serviceName"] for service in payload["services"]] == [
        "nomad_qdrant",
        "nomad_ollama",
        "nomad_cyberchef",
        "nomad_maps",
        "nomad_kiwix_server",
    ]
    assert payload["summary"]["totalEstimatedStorageMb"] == 3882
    assert payload["summary"]["totalEstimatedStorageLabel"] == "3.8 GB"
