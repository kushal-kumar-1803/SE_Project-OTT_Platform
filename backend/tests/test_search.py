from backend.app import app

client = app.test_client()

def test_search_movies_empty():
    response = client.get("/movies/search?q=")
    assert response.status_code == 200
    assert response.json["results"] == []


def test_search_movies_valid():
    response = client.get("/movies/search?q=frozen")
    assert response.status_code == 200
    assert "results" in response.json
