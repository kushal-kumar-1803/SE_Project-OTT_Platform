# backend/routes/profile_routes.py

from flask import Blueprint, request, jsonify
from backend.database.db_connection import get_db_connection

profiles_bp = Blueprint("profiles", __name__)

# Get all profiles for a user
@profiles_bp.route("/list/<int:user_id>", methods=["GET"])
def list_profiles(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute("SELECT id, name, avatar, is_kid, created_at FROM profiles WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    results = [dict(row) for row in rows]
    return jsonify({"profiles": results})

# Create profile
@profiles_bp.route("/create", methods=["POST"])
def create_profile():
    data = request.get_json()
    user_id = data.get("user_id")
    name = data.get("name")
    avatar = data.get("avatar", "")
    is_kid = 1 if data.get("is_kid") else 0

    if not user_id or not name:
        return jsonify({"error": "user_id and name required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO profiles (user_id, name, avatar, is_kid) VALUES (?, ?, ?, ?)",
                (user_id, name, avatar, is_kid))
    conn.commit()
    profile_id = cur.lastrowid
    conn.close()
    return jsonify({"message": "Profile created", "profile_id": profile_id}), 201

# Get single profile
@profiles_bp.route("/<int:profile_id>", methods=["GET"])
def get_profile(profile_id):
    conn = get_db_connection()
    row = conn.cursor().execute("SELECT id, user_id, name, avatar, is_kid, created_at FROM profiles WHERE id=?", (profile_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify(dict(row))

# Edit profile
@profiles_bp.route("/<int:profile_id>/edit", methods=["POST"])
def edit_profile(profile_id):
    data = request.get_json()
    name = data.get("name")
    avatar = data.get("avatar", None)
    is_kid = data.get("is_kid", None)

    conn = get_db_connection()
    cur = conn.cursor()

    # Build dynamic update
    parts = []
    params = []
    if name is not None:
        parts.append("name=?"); params.append(name)
    if avatar is not None:
        parts.append("avatar=?"); params.append(avatar)
    if is_kid is not None:
        parts.append("is_kid=?"); params.append(1 if is_kid else 0)

    if parts:
        params.append(profile_id)
        cur.execute(f"UPDATE profiles SET {', '.join(parts)} WHERE id=?", params)
        conn.commit()

    conn.close()
    return jsonify({"message": "Profile updated"})


# Delete profile
@profiles_bp.route("/<int:profile_id>/delete", methods=["POST"])
def delete_profile(profile_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM profile_watchlist WHERE profile_id=?", (profile_id,))
    cur.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Profile deleted"})


# -------------------------
# Profile watchlist endpoints
# -------------------------
@profiles_bp.route("/<int:profile_id>/watchlist", methods=["GET"])
def get_profile_watchlist(profile_id):
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute("SELECT movie_id, added_at FROM profile_watchlist WHERE profile_id=?", (profile_id,)).fetchall()
    conn.close()
    results = [{"movie_id": r["movie_id"], "added_at": r["added_at"]} for r in rows]
    return jsonify({"watchlist": results})

@profiles_bp.route("/<int:profile_id>/watchlist/add", methods=["POST"])
def add_watchlist(profile_id):
    data = request.get_json()
    movie_id = data.get("movie_id")
    if not movie_id:
        return jsonify({"error":"movie_id required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    # avoid duplicates
    existing = cur.execute("SELECT id FROM profile_watchlist WHERE profile_id=? AND movie_id=?", (profile_id, movie_id)).fetchone()
    if existing:
        conn.close()
        return jsonify({"message":"Already in watchlist"}), 200

    cur.execute("INSERT INTO profile_watchlist (profile_id, movie_id) VALUES (?, ?)", (profile_id, movie_id))
    conn.commit()
    conn.close()
    return jsonify({"message":"Added to profile watchlist"}), 201

@profiles_bp.route("/<int:profile_id>/watchlist/remove", methods=["POST"])
def remove_watchlist(profile_id):
    data = request.get_json()
    movie_id = data.get("movie_id")
    if not movie_id:
        return jsonify({"error":"movie_id required"}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM profile_watchlist WHERE profile_id=? AND movie_id=?", (profile_id, movie_id))
    conn.commit()
    conn.close()
    return jsonify({"message":"Removed from profile watchlist"})
