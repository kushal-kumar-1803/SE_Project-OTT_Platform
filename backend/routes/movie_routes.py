# backend/routes/movie_routes.py
import os
from flask import Blueprint, request, jsonify, send_file
from backend.database.db_connection import get_db_connection
from backend.services.tmdb_service import (
    search_movies as tmdb_search,
    get_movie_detail,
    get_image_url,
    get_movie_trailer  # ✅ IMPORTANT FIX
)

movie_bp = Blueprint("movies", __name__)


# ============================================================
# 1) LOCAL DATABASE SEARCH  --> /movies/search?q=
# ============================================================
@movie_bp.route("/search", methods=["GET"])
def search_local():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify({"results": []})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, genre, description
        FROM movies
        WHERE LOWER(title) LIKE ? OR LOWER(genre) LIKE ?
    """, (f"%{query}%", f"%{query}%"))

    rows = cursor.fetchall()
    conn.close()

    results = [
        {
            "id": row["id"],
            "title": row["title"],
            "genre": row["genre"],
            "poster": "/assets/images/default_poster.jpg"
        }
        for row in rows
    ]

    return jsonify({"results": results})


# ============================================================
# 2) TMDB SEARCH  --> /movies/tmdb_search?q=
# ============================================================
@movie_bp.route("/tmdb_search", methods=["GET"])
def tmdb_search_route():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"results": []})

    data = tmdb_search(query)
    results = []

    for m in data.get("results", []):
        results.append({
            "id": m.get("id"),
            "title": m.get("title"),
            "poster": get_image_url(m.get("poster_path"), "w500"),
            "overview": m.get("overview")
        })

    return jsonify({"results": results})


# ============================================================
# 3) GET MOVIE TRAILER FIRST  --> /movies/trailer/<id>
# (MUST COME BEFORE '/movies/<id>')
# ============================================================
@movie_bp.route('/trailer/<int:movie_id>', methods=['GET'])
def movie_trailer(movie_id):
    return get_movie_trailer(movie_id)



# ============================================================
# 4) TMDB MOVIE DETAIL  --> /movies/<id>
# ============================================================
@movie_bp.route("/<int:movie_id>", methods=["GET"])
def tmdb_detail(movie_id):
    data = get_movie_detail(movie_id)

    if not data or "id" not in data:
        return jsonify({"error": "Movie not found"}), 404

    return jsonify({
        "id": data.get("id"),
        "title": data.get("title"),
        "overview": data.get("overview"),
        "genres": [g["name"] for g in data.get("genres", [])],
        "release_date": data.get("release_date"),
        "rating": data.get("vote_average"),
        "poster": get_image_url(data.get("poster_path"), "w500"),
        "backdrop": get_image_url(data.get("backdrop_path"), "original")
    })

@movie_bp.route("/stream/<int:movie_id>")
def stream_movie(movie_id):

    # Map movie ID → local video file
    if movie_id == 109445:
        video_path = "../../frontend/assets/videos/frozen.mp4"
    else:
        return {"error": "Movie not found"}, 404

    # Build absolute path
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), video_path))

    if not os.path.exists(abs_path):
        return {
            "error": "File not found",
            "looked_for": abs_path
        }, 404

    return send_file(abs_path, mimetype="video/mp4")

@movie_bp.route("/all", methods=["GET"])
def get_all_local_movies():
    conn = get_db_connection()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT id, title, genre, description, poster_url, video_url
        FROM movies
    """).fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "title": row["title"],
            "genre": row["genre"],
            "description": row["description"],
            "poster_url": row["poster_url"] or "/assets/images/default_poster.jpg",
            "video_url": row["video_url"]
        })

    return jsonify({"results": results})
