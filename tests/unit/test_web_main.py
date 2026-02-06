from fastapi.testclient import TestClient

from fishing_analyzer.web.main import app


def test_dashboard_page_returns_html() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "Fishing Analyzer" in response.text
    assert 'id="dashboard-content"' in response.text


def test_dashboard_partial_returns_fragment() -> None:
    client = TestClient(app)

    response = client.get("/partials/dashboard")

    assert response.status_code == 200
    assert "Recent catches" in response.text
    assert "<html" not in response.text.lower()


def test_dashboard_partial_handles_empty_result() -> None:
    client = TestClient(app)

    response = client.get(
        "/partials/dashboard",
        params={"year": 1900, "fish_type": "__not_existing__"},
    )

    assert response.status_code == 200
    assert "No catches for this filter." in response.text
