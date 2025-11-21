import sqlite3

DB_NAME = "ott_platform.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user',
        reset_token TEXT,
        reset_expiry TEXT
    );

    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        description TEXT,
        video_url TEXT,
        poster_url TEXT   -- ⭐ NEW COLUMN ⭐
    );

    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan TEXT,
        start_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS watch_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        watched_at TEXT,
        watch_duration INTEGER,
        resume_position INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    );

    CREATE TABLE IF NOT EXISTS watchlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        added_at TEXT,
        UNIQUE(user_id, movie_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    );

    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        rating REAL,
        review TEXT,
        rated_at TEXT,
        UNIQUE(user_id, movie_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    );
    """)

    conn.commit()
    conn.close()
