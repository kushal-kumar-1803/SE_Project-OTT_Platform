import sqlite3
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ott_platform.db")


def get_db_connection():
    print("📌 USING DB:", DB_PATH)  # Debug line
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # existing tables
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
        poster_url TEXT
    );

     CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan TEXT,
        status TEXT DEFAULT 'pending',
        start_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

                        
    CREATE TABLE IF NOT EXISTS payment_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plan TEXT,
    amount INTEGER,
    status TEXT DEFAULT 'pending',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
    """)

    # -------------------------
    # Profiles (multi-profile)
    # -------------------------
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        avatar TEXT,
        is_kid INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS profile_watchlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        added_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(profile_id) REFERENCES profiles(id)
    );
    """)

    conn.commit()
    conn.close()

    
