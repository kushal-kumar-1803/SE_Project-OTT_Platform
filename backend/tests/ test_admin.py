import io
from backend.app import app

client = app.test_client()

def test_admin_add_movie():
    data = {
        "title": "PyTest Movie",
        "genre": "Action",
        "description": "Test Description",
        "video": (io.BytesIO(b"dummydata"), "test.mp4")
    }
    response = client.post(
        "/admin-api/add_movie",
        data=data,
        content_type="multipart/form-data"
    )
    assert response.status_code in [200, 201]
