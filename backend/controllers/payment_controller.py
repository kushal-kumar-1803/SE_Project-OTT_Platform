from flask import request, jsonify
from backend.database.db_connection import get_db_connection

def create_payment_request():
    data = request.get_json()
    user_id = data.get("user_id")
    plan = data.get("plan")
    amount = data.get("amount")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO payment_requests (user_id, plan, amount)
        VALUES (?, ?, ?)
    """, (user_id, plan, amount))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

def get_pending_payments():
    conn = get_db_connection()
    cursor = conn.cursor()

    data = cursor.execute("""
        SELECT * FROM payment_requests WHERE status='pending'
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])


def approve_payment():
    data = request.get_json()
    payment_id = data.get("payment_id")
    user_id = data.get("user_id")
    plan = data.get("plan")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Update payment status
    cursor.execute("""
        UPDATE payment_requests SET status='approved' WHERE id=?
    """, (payment_id,))

    # Create subscription
    cursor.execute("""
        INSERT INTO subscriptions (user_id, plan, start_date)
        VALUES (?, ?, date('now'))
    """, (user_id, plan))

    conn.commit()
    conn.close()

    return jsonify({"success": True})
