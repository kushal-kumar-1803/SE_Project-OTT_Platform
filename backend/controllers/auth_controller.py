from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.db_connection import get_db_connection
from backend.services.jwt_services import generate_token

def register_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    hashed_pw = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                   (name, email, hashed_pw))
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully!"}), 201

def login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        token = generate_token(user['id'])
        return jsonify({"token": token, "user_id": user['id']}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
