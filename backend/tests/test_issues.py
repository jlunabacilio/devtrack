from fastapi.testclient import TestClient


def _create(client: TestClient, title: str, **kwargs) -> dict:
    resp = client.post("/issues", json={"title": title, **kwargs})
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_create_issue_defaults_to_open(client: TestClient) -> None:
    issue = _create(client, "Fix login bug")
    assert issue["id"] > 0
    assert issue["title"] == "Fix login bug"
    assert issue["status"] == "open"


def test_get_issue(client: TestClient) -> None:
    created = _create(client, "Write docs")
    resp = client.get(f"/issues/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Write docs"


def test_get_missing_issue_returns_404(client: TestClient) -> None:
    resp = client.get("/issues/999")
    assert resp.status_code == 404


def test_update_issue_status(client: TestClient) -> None:
    created = _create(client, "Refactor service")
    resp = client.patch(
        f"/issues/{created['id']}", json={"status": "in_progress"}
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"


def test_delete_issue(client: TestClient) -> None:
    created = _create(client, "Remove dead code")
    assert client.delete(f"/issues/{created['id']}").status_code == 204
    assert client.get(f"/issues/{created['id']}").status_code == 404


def test_list_all_issues(client: TestClient) -> None:
    _create(client, "Issue A")
    _create(client, "Issue B")
    resp = client.get("/issues")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_list_filters_by_status(client: TestClient) -> None:
    open_issue = _create(client, "Still open")
    closed = _create(client, "Already closed")
    client.patch(f"/issues/{closed['id']}", json={"status": "closed"})

    resp = client.get("/issues", params={"status": "open"})
    assert resp.status_code == 200

    titles = [i["title"] for i in resp.json()]
    assert titles == [open_issue["title"]]
