from unittest.mock import MagicMock, patch

import pytest

from app.core.config import get_settings

pytestmark = [pytest.mark.integration, pytest.mark.knowledge_base]


def test_rag_upload_indexes_file_and_exposes_status(client) -> None:
    response = client.post(
        "/api/rag/upload",
        files={
            "file": (
                "field-guide.txt",
                b"Atlas Haven caches field guides locally.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["alreadyProcessing"] is False

    files = client.get("/api/rag/files")
    assert files.status_code == 200
    assert payload["filePath"] in files.json()["files"]

    status = client.get("/api/rag/job-status", params={"filePath": payload["filePath"]})
    assert status.status_code == 200
    assert status.json()["status"] == "completed"

    active_jobs = client.get("/api/rag/active-jobs")
    assert active_jobs.status_code == 200
    assert active_jobs.json() == []

    deleted = client.request("DELETE", "/api/rag/files", json={"source": payload["filePath"]})
    assert deleted.status_code == 200
    assert payload["filePath"] not in client.get("/api/rag/files").json()["files"]


@patch("app.modules.ollama.service.httpx.post")
@patch("app.modules.ollama.service.subprocess.run", return_value=MagicMock(returncode=0))
@patch("app.modules.ollama.service.shutil.which", return_value="/fake/ollama")
def test_rag_sync_indexes_existing_files_and_chat_uses_context(
    mock_which, mock_run, mock_post, client,
) -> None:
    class _ChatResp:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "message": {
                    "role": "assistant",
                    "content": "Use pacific-plan.txt for deployment preload.",
                }
            }

    mock_post.return_value = _ChatResp()

    storage_root = get_settings().storage_path / "rag" / "files"
    storage_root.mkdir(parents=True, exist_ok=True)
    source = storage_root / "pacific-plan.txt"
    source.write_text("Pacific deployment plans should preload offline maps and medical documents.")

    sync = client.post("/api/rag/sync")

    assert sync.status_code == 200
    assert sync.json()["success"] is True
    assert sync.json()["filesQueued"] == 1

    client.post("/api/ollama/models", json={"model": "llama3.2:1b-text-q2_K"})
    response = client.post(
        "/api/ollama/chat",
        json={
            "model": "llama3.2:1b-text-q2_K",
            "messages": [
                {
                    "role": "user",
                    "content": "What should I preload for a pacific deployment?",
                }
            ],
        },
    )

    assert response.status_code == 200
    assert "pacific-plan.txt" in response.json()["message"]["content"]
