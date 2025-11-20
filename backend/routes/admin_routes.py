# ==========================================
# FILE 1: backend/routes/admin_routes.py
# ==========================================
from flask import Blueprint, request, jsonify
from backend.database.db_connection import get_db_connection
from backend.controllers.admin_controller import (
    add_movie,
    update_movie,
    delete_movie,
    get_all_movies_admin
)

admin_bp = Blueprint("admin", __name__)

# POST /admin-api/movies/add
@admin_bp.route("/movies/add", methods=["POST"])
def add_movie_route():
    return add_movie()

# GET /admin-api/movies/all
@admin_bp.route("/movies/all", methods=["GET"])
def get_movies_route():
    return get_all_movies_admin()

# DELETE /admin-api/movies/delete/<id>
@admin_bp.route("/movies/delete/<int:movie_id>", methods=["DELETE"])
def delete_movie_route(movie_id):
    return delete_movie(movie_id)

# PUT /admin-api/movies/update/<id>
@admin_bp.route("/movies/update/<int:movie_id>", methods=["PUT"])
def update_movie_route(movie_id):
    return update_movie(movie_id)

@admin_bp.route("/approve-payment", methods=["POST"])
def approve_payment():
    data = request.get_json()
    payment_id = data["payment_id"]
    user_id = data["user_id"]
    plan = data["plan"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # Update subscription table to active
    cursor.execute("""
        UPDATE subscriptions
        SET status = 'active'
        WHERE id = ?
    """, (payment_id,))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

