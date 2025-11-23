from flask import request, jsonify
from backend.database.db_connection import get_db_connection

# ✅ Add a new movie
def add_movie():
    data = request.get_json()
    title = data.get('title')
    genre = data.get('genre')
    description = data.get('description', '')
    video_url = data.get('video_url')
    poster_url = data.get('poster_url', '')

    if not title or not genre or not video_url:
        return jsonify({"error": "Title, genre, and video URL are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO movies (title, genre, description, video_url, poster_url) VALUES (?, ?, ?, ?, ?)",
            (title, genre, description, video_url, poster_url)
        )
        conn.commit()
        movie_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": f"Movie '{title}' added successfully!",
            "movie_id": movie_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Update an existing movie
def update_movie(movie_id):
    data = request.get_json()
    title = data.get('title')
    genre = data.get('genre')
    description = data.get('description', '')
    video_url = data.get('video_url')
    poster_url = data.get('poster_url', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE movies 
            SET title=?, genre=?, description=?, video_url=?, poster_url=?
            WHERE id=?
        """, (title, genre, description, video_url, poster_url, movie_id))

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Movie not found"}), 404

        conn.commit()
        conn.close()
        return jsonify({"message": f"Movie ID {movie_id} updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Delete a movie
def delete_movie(movie_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Movie not found"}), 404
            
        conn.commit()
        conn.close()

        return jsonify({"message": f"Movie ID {movie_id} deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Get all movies (admin view)
def get_all_movies_admin():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        movies = cursor.execute("SELECT * FROM movies ORDER BY id DESC").fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in movies]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500