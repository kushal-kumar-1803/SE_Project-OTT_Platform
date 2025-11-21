from backend.app import app

client = app.test_client()

def test_stream_movie():
    response = client.get("/movies/stream/1")
    assert response.status_code in [200, 404]  
