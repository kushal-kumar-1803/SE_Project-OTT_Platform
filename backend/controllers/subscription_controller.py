from flask import request, jsonify
from backend.database.db_connection import get_db_connection

# ✅ Function 1: Subscribe a new user
def subscribe_user():
    data = request.get_json()
    user_id = data.get('user_id')
    plan = data.get('plan')

    if not user_id or not plan:
        return jsonify({"error": "Missing user_id or plan"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subscriptions (user_id, plan, start_date) VALUES (?, ?, DATE('now'))",
        (user_id, plan)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"User {user_id} subscribed to {plan} plan successfully!"}), 201


# ✅ Function 2: Get all subscriptions
def get_subscriptions():
    conn = get_db_connection()
    cursor = conn.cursor()
    subs = cursor.execute("SELECT * FROM subscriptions").fetchall()
    conn.close()
    return jsonify([dict(row) for row in subs])
