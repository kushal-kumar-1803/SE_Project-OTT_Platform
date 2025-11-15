from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.db_connection import get_db_connection
from backend.services.jwt_services import generate_token
import sqlite3

# -----------------------------
# REGISTER USER
# -----------------------------
def register_user():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Validate fields
    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_pw = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_pw)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except sqlite3.IntegrityError:
        # UNIQUE constraint failed: users.email
        return jsonify({"error": "Email already registered"}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()


# -----------------------------
# LOGIN USER
# -----------------------------
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()

    conn.close()

    if user and check_password_hash(user['password'], password):
        token = generate_token(user['id'])
        return jsonify({
            "token": token,
            "user_id": user['id'],
            "message": "Login successful"
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401
