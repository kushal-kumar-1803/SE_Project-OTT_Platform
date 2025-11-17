# backend/controllers/movie_controller.py

from flask import request, jsonify
from backend.database.db_connection import get_db_connection
from backend.services.tmdb_service import (
    get_movie_detail,
    search_movies as tmdb_search,
    get_image_url
)

# -----------------------------
# LOCAL DB MOVIES
# -----------------------------
def get_all_movies():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()

    return jsonify({"results": [dict(row) for row in movies]})


def search_local_movies():
    query = request.args.get("q", "").lower().strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT id, title, genre, description
        FROM movies
        WHERE LOWER(title) LIKE ? OR LOWER(genre) LIKE ?
    """, (f"%{query}%", f"%{query}%")).fetchall()

    conn.close()

    results = [
        {
            "id": row["id"],
            "title": row["title"],
            "genre": row["genre"],
            "poster": "https://placehold.co/300x450?text=" + row["title"]
        }
        for row in rows
    ]

    return jsonify({"results": results})


# -----------------------------
# TMDB MOVIES
# -----------------------------
def get_tmdb_movie(movie_id):
    data = get_movie_detail(movie_id)

    return jsonify({
        "id": data.get("id"),
        "title": data.get("title"),
        "overview": data.get("overview"),
        "genres": [g["name"] for g in data.get("genres", [])],
        "poster": get_image_url(data.get("poster_path"), "w500"),
        "backdrop": get_image_url(data.get("backdrop_path"), "original")
    })


def search_tmdb_movies():
    query = request.args.get("q", "").strip()
    data = tmdb_search(query)

    results = [
        {
            "id": m["id"],
            "title": m["title"],
            "poster": get_image_url(m.get("poster_path"), "w500")
        }
        for m in data.get("results", [])
    ]

    return jsonify({"results": results})

def get_movie_trailer(movie_id):
    data = get_movie_videos(movie_id)

    if "results" not in data:
        return jsonify({"error": "No videos found"}), 404

    # Filter for official YouTube trailers
    for video in data["results"]:
        if video["site"] == "YouTube" and video["type"] in ["Trailer", "Teaser"]:
            return jsonify({"youtube_key": video["key"]})

    # fallback: return first YouTube video
    for video in data["results"]:
        if video["site"] == "YouTube":
            return jsonify({"youtube_key": video["key"]})

    return jsonify({"error": "Trailer not available"}), 404

