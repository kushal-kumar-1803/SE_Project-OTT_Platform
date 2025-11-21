# backend/routes/movie_routes.py

from flask import Blueprint, request, jsonify
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
    # Demo movie file
    return """
    <h1 style='color:white'>Streaming Full Movie (Demo)</h1>
    <video width='900' controls autoplay>
      <source src='/assets/movies/demo.mp4' type='video/mp4'>
    </video>
    """
