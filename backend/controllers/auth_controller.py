# backend/controllers/auth_controller.py

from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_mail import Message
import sqlite3
import random
import string

from backend.database.db_connection import get_db_connection
from backend.services.jwt_services import generate_token
from backend.extensions import mail


# GENERATE OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


# REGISTER USER
def register_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    hashed_pw = generate_password_hash(password)

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, hashed_pw, 'user')
        )
        conn.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409

    finally:
        conn.close()


# LOGIN USER
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    user = cur.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user["id"])
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user["id"],
        "role": user["role"] if user["role"] else "user"
    }), 200


# FORGOT PASSWORD (SEND OTP)
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    conn = get_db_connection()
    cur = conn.cursor()

    user = cur.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not user:
        return jsonify({"error": "Email not found"}), 404

    otp = generate_otp()
    expiry = (datetime.utcnow() + timedelta(minutes=10)).isoformat()

    cur.execute(
        "UPDATE users SET reset_token=?, reset_expiry=? WHERE email=?",
        (otp, expiry, email)
    )
    conn.commit()
    conn.close()

    msg = Message(
        subject="OTT Password Reset Code",
        sender="mdsadatullah97@gmail.com",
        recipients=[email],
        body=f"Your OTP is: {otp}\nValid for 10 minutes."
    )
    mail.send(msg)

    return jsonify({"message": "OTP sent to email"}), 200


# RESET PASSWORD
def reset_password():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("new_password")

    conn = get_db_connection()
    cur = conn.cursor()

    user = cur.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not user:
        return jsonify({"error": "Invalid email"}), 404

    if user["reset_token"] != otp:
        return jsonify({"error": "Invalid OTP"}), 400

    if datetime.utcnow() > datetime.fromisoformat(user["reset_expiry"]):
        return jsonify({"error": "OTP expired"}), 400

    hashed_pw = generate_password_hash(new_password)

    cur.execute(
        "UPDATE users SET password=?, reset_token=NULL, reset_expiry=NULL WHERE email=?",
        (hashed_pw, email)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Password reset successful"}), 200
