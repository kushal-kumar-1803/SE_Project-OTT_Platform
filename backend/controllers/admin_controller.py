from flask import request, jsonify
from backend.database.db_connection import get_db_connection

# ✅ Add a new movie
def add_movie():
    data = request.get_json()
    title = data.get('title')
    genre = data.get('genre')
    description = data.get('description')
    video_url = data.get('video_url')

    if not title or not genre:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO movies (title, genre, description, video_url) VALUES (?, ?, ?, ?)",
        (title, genre, description, video_url)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"Movie '{title}' added successfully!"}), 201


# ✅ Update an existing movie
def update_movie(movie_id):
    data = request.get_json()
    title = data.get('title')
    genre = data.get('genre')
    description = data.get('description')
    video_url = data.get('video_url')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE movies 
        SET title=?, genre=?, description=?, video_url=? 
        WHERE id=?
    """, (title, genre, description, video_url, movie_id))

    conn.commit()
    conn.close()
    return jsonify({"message": f"Movie ID {movie_id} updated successfully!"}), 200


# ✅ Delete a movie
def delete_movie(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Movie ID {movie_id} deleted successfully!"}), 200


# ✅ Get all movies (admin view)
def get_all_movies_admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    movies = cursor.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return jsonify([dict(row) for row in movies])
