from flask import request, jsonify
from backend.database.db_connection import get_db_connection

def get_all_movies():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return jsonify([dict(row) for row in movies])

def search_movies():
    query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    movies = cursor.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + query + '%',)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in movies])
