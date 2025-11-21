from flask import Blueprint, request, jsonify
from backend.database.db_connection import get_db_connection
from datetime import datetime

sub_bp = Blueprint("sub_bp", __name__)

# -----------------------------------------------------------
# 1. ACTIVATE SUBSCRIPTION (when user pays)
# -----------------------------------------------------------
@sub_bp.route("/activate", methods=["POST"])
def activate_subscription():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        plan = data.get("plan")

        if not user_id or not plan:
            return jsonify({"error": "Missing user_id or plan"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO subscriptions (user_id, plan, status, start_date)
            VALUES (?, ?, 'pending', ?)
        """, (user_id, plan, datetime.now().strftime("%Y-%m-%d")))

        conn.commit()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print("ACTIVATE ERROR:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# 2. FETCH USER SUBSCRIPTION STATUS
# -----------------------------------------------------------
@sub_bp.route("/status/<int:user_id>")
def subscription_status(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sub = cursor.execute("""
            SELECT id, plan, status 
            FROM subscriptions 
            WHERE user_id=? 
            ORDER BY id DESC 
            LIMIT 1
        """, (user_id,)).fetchone()

        conn.close()

        if not sub:
            return jsonify({"subscribed": False})

        return jsonify({
            "id": sub["id"],
            "plan": sub["plan"],
            "status": sub["status"],
            "subscribed": sub["status"] == "approved"
        })

    except Exception as e:
        print("STATUS ERROR:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# 3. LIST ALL PENDING SUBSCRIPTIONS (ADMIN PANEL DISPLAY)
# -----------------------------------------------------------
@sub_bp.route("/pending", methods=["GET"])
def pending_subscriptions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        rows = cursor.execute("""
            SELECT id, user_id, plan, start_date, status
            FROM subscriptions
            WHERE status = 'pending'
            ORDER BY id DESC
        """).fetchall()

        conn.close()

        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "user_id": r["user_id"],
                "plan": r["plan"],
                "amount": get_plan_amount(r["plan"]),   # pricing helper
                "status": r["status"],
                "start_date": r["start_date"]
            })

        return jsonify(result)

    except Exception as e:
        print("PENDING ERROR:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------
# 4. ADMIN APPROVES A SUBSCRIPTION
# -----------------------------------------------------------
@sub_bp.route("/approve/<int:sub_id>", methods=["PUT"])
def approve_subscription(sub_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE subscriptions 
            SET status='approved'
            WHERE id=?
        """, (sub_id,))

        conn.commit()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print("APPROVE ERROR:", e)
        return jsonify({"error": str(e)}), 500



# -----------------------------------------------------------
# OPTIONAL — PLAN PRICE LOOKUP
# -----------------------------------------------------------
def get_plan_amount(plan):
    prices = {
        "Basic": 199,
        "Standard": 399,
        "Premium": 599,
        "Ultra": 799
    }
    return prices.get(plan, 0)
