# backend/controllers/movie_controller.py

from flask import request, jsonify
from backend.database.db_connection import get_db_connection
from backend.services.tmdb_service import get_movie_detail, search_movies as tmdb_search, get_image_url


# -------------------------
# LOCAL DB MOVIE FUNCTIONS
# -------------------------

def get_all_movies():
    """Return movies stored in your local SQLite DB."""
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()

    return jsonify([dict(row) for row in movies])


def search_local_movies():
    """Search movies stored in local DB."""
    query = request.args.get('q', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    movies = cursor.execute(
        "SELECT * FROM movies WHERE title LIKE ?",
        (f"%{query}%",)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in movies])


# -------------------------
# TMDB MOVIE FUNCTIONS
# -------------------------

def get_tmdb_movie(movie_id):
    """Return a TMDB movie detail."""
    try:
        data = get_movie_detail(movie_id)

        result = {
            "id": data.get("id"),
            "title": data.get("title"),
            "overview": data.get("overview"),
            "genres": [g["name"] for g in data.get("genres", [])],
            "release_date": data.get("release_date"),
            "runtime": data.get("runtime"),
            "rating": data.get("vote_average"),
            "poster": get_image_url(data.get("poster_path"), size="w500"),
            "backdrop": get_image_url(data.get("backdrop_path"), size="original")
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Failed to fetch TMDB movie", "details": str(e)}), 500


def search_tmdb_movies():
    """Search movies using TMDB API."""
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"results": []})

    try:
        data = tmdb_search(query)

        results = []
        for m in data.get("results", []):
            results.append({
                "id": m.get("id"),
                "title": m.get("title"),
                "poster": get_image_url(m.get("poster_path"), "w500"),
                "overview": m.get("overview"),
                "release_date": m.get("release_date")
            })

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": "TMDB search failed", "details": str(e)}), 500
