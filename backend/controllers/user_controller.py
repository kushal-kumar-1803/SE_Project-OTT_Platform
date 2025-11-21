# backend/controllers/user_controller.py
"""
User features: watch history, watchlist, ratings, resume playback
Aligns with OTT-F-040, OTT-F-050 from test plan
"""

from flask import request, jsonify
from datetime import datetime
from backend.database.db_connection import get_db_connection

# ========================================
# WATCH HISTORY (OTT-F-040)
# ========================================

def add_to_watch_history():
    """
    Add/update watch history for a user
    POST /user/watch-history
    Body: {user_id, movie_id, watch_duration, resume_position}
    """
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        movie_id = data.get("movie_id")
        watch_duration = data.get("watch_duration", 0)
        resume_position = data.get("resume_position", 0)
        
        if not user_id or not movie_id:
            return jsonify({"error": "user_id and movie_id required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if entry exists
        existing = cursor.execute(
            "SELECT id FROM watch_history WHERE user_id=? AND movie_id=?",
            (user_id, movie_id)
        ).fetchone()

        if existing:
            # Update existing entry
            cursor.execute("""
                UPDATE watch_history 
                SET watched_at=?, watch_duration=?, resume_position=?
                WHERE user_id=? AND movie_id=?
            """, (datetime.utcnow().isoformat(), watch_duration, resume_position, user_id, movie_id))
        else:
            # Insert new entry
            cursor.execute("""
                INSERT INTO watch_history (user_id, movie_id, watched_at, watch_duration, resume_position)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, movie_id, datetime.utcnow().isoformat(), watch_duration, resume_position))

        conn.commit()
        conn.close()

        return jsonify({"message": "Watch history updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_watch_history():
    """
    Get user's watch history
    GET /user/watch-history?user_id=<id>
    """
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        history = cursor.execute("""
            SELECT wh.id, wh.user_id, wh.movie_id, m.title, m.poster_url, 
                   wh.watched_at, wh.watch_duration, wh.resume_position
            FROM watch_history wh
            JOIN movies m ON wh.movie_id = m.id
            WHERE wh.user_id = ?
            ORDER BY wh.watched_at DESC
            LIMIT 50
        """, (user_id,)).fetchall()

        conn.close()

        return jsonify({
            "watch_history": [dict(row) for row in history]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_resume_position():
    """
    Get resume position for a specific movie
    GET /user/resume?user_id=<id>&movie_id=<id>
    """
    try:
        user_id = request.args.get("user_id")
        movie_id = request.args.get("movie_id")

        if not user_id or not movie_id:
            return jsonify({"error": "user_id and movie_id required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        row = cursor.execute("""
            SELECT resume_position, watch_duration 
            FROM watch_history 
            WHERE user_id=? AND movie_id=?
        """, (user_id, movie_id)).fetchone()

        conn.close()

        if row:
            return jsonify({
                "resume_position": row["resume_position"],
                "watch_duration": row["watch_duration"]
            }), 200
        else:
            return jsonify({"resume_position": 0, "watch_duration": 0}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================================
# WATCHLIST (OTT-F-050)
# ========================================

def add_to_watchlist():
    """
    Add movie to watchlist
    POST /user/watchlist
    Body: {user_id, movie_id}
    """
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        movie_id = data.get("movie_id")

        if not user_id or not movie_id:
            return jsonify({"error": "user_id and movie_id required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if already in watchlist
        existing = cursor.execute(
            "SELECT id FROM watchlist WHERE user_id=? AND movie_id=?",
            (user_id, movie_id)
        ).fetchone()

        if existing:
            conn.close()
            return jsonify({"message": "Already in watchlist"}), 200

        cursor.execute("""
            INSERT INTO watchlist (user_id, movie_id, added_at)
            VALUES (?, ?, ?)
        """, (user_id, movie_id, datetime.utcnow().isoformat()))

        conn.commit()
        conn.close()

        return jsonify({"message": "Added to watchlist"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def remove_from_watchlist():
    """
    Remove movie from watchlist
    DELETE /user/watchlist/<watchlist_id>
    """
    try:
        watchlist_id = request.args.get("watchlist_id")
        user_id = request.args.get("user_id")

        if not watchlist_id or not user_id:
            return jsonify({"error": "watchlist_id and user_id required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verify ownership
        row = cursor.execute(
            "SELECT user_id FROM watchlist WHERE id=?",
            (watchlist_id,)
        ).fetchone()

        if not row or row["user_id"] != int(user_id):
            conn.close()
            return jsonify({"error": "Unauthorized"}), 403

        cursor.execute("DELETE FROM watchlist WHERE id=?", (watchlist_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Removed from watchlist"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_watchlist():
    """
    Get user's watchlist
    GET /user/watchlist?user_id=<id>
    """
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        watchlist = cursor.execute("""
            SELECT w.id, w.user_id, w.movie_id, m.title, m.genre, 
                   m.description, m.poster_url, w.added_at
            FROM watchlist w
            JOIN movies m ON w.movie_id = m.id
            WHERE w.user_id = ?
            ORDER BY w.added_at DESC
        """, (user_id,)).fetchall()

        conn.close()

        return jsonify({
            "watchlist": [dict(row) for row in watchlist]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================================
# RATINGS & REVIEWS (OTT-F-050)
# ========================================

def add_rating():
    """
    Add or update rating for a movie
    POST /user/rating
    Body: {user_id, movie_id, rating, review}
    """
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        movie_id = data.get("movie_id")
        rating = data.get("rating")
        review = data.get("review", "")

        if not user_id or not movie_id or rating is None:
            return jsonify({"error": "user_id, movie_id, and rating required"}), 400

        if not (0 <= float(rating) <= 10):
            return jsonify({"error": "Rating must be between 0-10"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if rating exists
        existing = cursor.execute(
            "SELECT id FROM ratings WHERE user_id=? AND movie_id=?",
            (user_id, movie_id)
        ).fetchone()

        if existing:
            # Update existing rating
            cursor.execute("""
                UPDATE ratings 
                SET rating=?, review=?, rated_at=?
                WHERE user_id=? AND movie_id=?
            """, (rating, review, datetime.utcnow().isoformat(), user_id, movie_id))
        else:
            # Insert new rating
            cursor.execute("""
                INSERT INTO ratings (user_id, movie_id, rating, review, rated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, movie_id, rating, review, datetime.utcnow().isoformat()))

        conn.commit()
        conn.close()

        return jsonify({"message": "Rating saved"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_movie_ratings():
    """
    Get all ratings for a movie with average score
    GET /user/movie-ratings?movie_id=<id>
    """
    try:
        movie_id = request.args.get("movie_id")
        if not movie_id:
            return jsonify({"error": "movie_id required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get all ratings
        ratings = cursor.execute("""
            SELECT r.id, r.user_id, r.rating, r.review, r.rated_at
            FROM ratings r
            WHERE r.movie_id = ?
            ORDER BY r.rated_at DESC
        """, (movie_id,)).fetchall()

        # Get average rating
        avg_row = cursor.execute("""
            SELECT AVG(rating) as avg_rating, COUNT(*) as total_ratings
            FROM ratings
            WHERE movie_id = ?
        """, (movie_id,)).fetchone()

        conn.close()

        return jsonify({
            "movie_id": movie_id,
            "ratings": [dict(row) for row in ratings],
            "average_rating": avg_row["avg_rating"] or 0,
            "total_ratings": avg_row["total_ratings"] or 0
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_user_rating():
    """
    Get a specific user's rating for a movie
    GET /user/rating?user_id=<id>&movie_id=<id>
    """
    try:
        user_id = request.args.get("user_id")
        movie_id = request.args.get("movie_id")

        if not user_id or not movie_id:
            return jsonify({"error": "user_id and movie_id required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        row = cursor.execute("""
            SELECT id, rating, review, rated_at
            FROM ratings
            WHERE user_id=? AND movie_id=?
        """, (user_id, movie_id)).fetchone()

        conn.close()

        if row:
            return jsonify(dict(row)), 200
        else:
            return jsonify({"rating": None, "review": None}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
