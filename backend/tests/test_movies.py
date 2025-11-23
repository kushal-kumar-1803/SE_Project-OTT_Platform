from backend.app import app

client = app.test_client()

def test_get_local_movies():
    response = client.get("/movies/all")
    assert response.status_code == 200
    data = response.json
    assert "results" in data
    assert type(data["results"]) == list
