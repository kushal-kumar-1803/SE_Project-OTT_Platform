# backend/services/auth_service.py
import os
import jwt
from functools import wraps
from flask import request, jsonify, current_app

JWT_SECRET = os.getenv("JWT_SECRET", "replace_with_strong_secret")
JWT_ALGO = "HS256"

def generate_token(user_id, expire_seconds=None):
    payload = {"user_id": user_id}
    # Add expiry if needed
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except Exception:
        return None

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth.split(" ", 1)[1]
        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        request.user = payload  # attach payload to request for later use
        return f(*args, **kwargs)
    return wrapper
