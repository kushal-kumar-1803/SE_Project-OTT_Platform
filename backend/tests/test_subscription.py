from backend.app import app

client = app.test_client()

def test_subscription_status():
    user_id = 1
    response = client.get(f"/subscriptions/status/{user_id}")
    assert response.status_code == 200
    assert "subscribed" in response.json
