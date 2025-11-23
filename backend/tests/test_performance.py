import time
from backend.app import app

client = app.test_client()

def test_api_performance():
    start = time.time()
    response = client.get("/movies/all")
    end = time.time()

    assert response.status_code == 200
    assert (end - start) < 3  # Must return within 3 seconds


def test_video_stream_latency():
    start = time.time()
    response = client.get("/movies/stream/1")
    end = time.time()

    assert response.status_code in [200, 404]
    assert (end - start) < 5  # Video load within 5 sec
