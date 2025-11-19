from flask import request, jsonify
from backend.database.db_connection import get_db_connection
from backend.services.tmdb_service import (
    get_movie_detail,
    search_movies as tmdb_search,
    get_image_url
)

# ---------------------------------------------------
# LOCAL MOVIES LIST
# ---------------------------------------------------
def get_all_movies():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return jsonify({"results": [dict(row) for row in movies]})


# ---------------------------------------------------
# LOCAL SEARCH
# ---------------------------------------------------
def search_local_movies():
    query = request.args.get("q", "").lower().strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    movies = cursor.execute("""
        SELECT id, title, genre, description
        FROM movies
        WHERE LOWER(title) LIKE ? OR LOWER(genre) LIKE ?
    """, (f"%{query}%", f"%{query}%")).fetchall()

    conn.close()

    results = []
    for m in movies:
        results.append({
            "id": m["id"],
            "title": m["title"],
            "genre": m["genre"],
            "poster": "https://placehold.co/300x450?text=" + m["title"]
        })

    return jsonify({"results": results})


# ---------------------------------------------------
# TMDB DETAIL
# ---------------------------------------------------
def get_tmdb_movie(movie_id):
    data = get_movie_detail(movie_id)

    return jsonify({
        "id": data["id"],
        "title": data.get("title"),
        "overview": data.get("overview"),
        "genres": [g["name"] for g in data.get("genres", [])],
        "poster": get_image_url(data.get("poster_path"), "w500"),
        "backdrop": get_image_url(data.get("backdrop_path"), "original")
    })


# ---------------------------------------------------
# TMDB SEARCH
# ---------------------------------------------------
def search_tmdb_movies():
    query = request.args.get("q", "").strip()
    data = tmdb_search(query)

    results = []
    for m in data.get("results", []):
        results.append({
            "id": m["id"],
            "title": m["title"],
            "poster": get_image_url(m.get("poster_path"), "w500")
        })

    return jsonify({"results": results})


# ---------------------------------------------------
# UNIFIED MOVIE DETAIL HANDLER
# local DB → else fallback to TMDB
# ---------------------------------------------------
def get_movie_by_id(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    movie = cursor.execute(
        "SELECT * FROM movies WHERE id = ?", (movie_id,)
    ).fetchone()

    conn.close()

    # Local DB movie found
    if movie:
        return jsonify({
            "id": movie["id"],
            "title": movie["title"],
            "overview": movie["description"],
            "genres": [movie["genre"]],
            "release_date": None,
            "rating": None,
            "poster": "/assets/images/default_poster.jpg",
            "backdrop": "/assets/images/default_backdrop.jpg"
        })

    # No local → fall back to TMDB
    return get_tmdb_movie(movie_id)
