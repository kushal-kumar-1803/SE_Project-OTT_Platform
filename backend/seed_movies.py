from backend.database.db_connection import get_db_connection

movies = [
    ("Inception", "Sci-Fi", "A thief enters people's dreams to steal secrets.", "https://sample.com/inception"),
    ("Interstellar", "Sci-Fi", "A team travels through a wormhole to save humanity.", "https://sample.com/interstellar"),
    ("The Dark Knight", "Action", "Batman faces the Joker in Gotham City.", "https://sample.com/darkknight"),
    ("Avatar", "Fantasy", "A marine on an alien planet becomes part of the Na'vi tribe.", "https://sample.com/avatar"),
    ("John Wick", "Action", "A retired assassin goes on a revenge rampage.", "https://sample.com/johnwick")
]

conn = get_db_connection()
cursor = conn.cursor()

for title, genre, desc, url in movies:
    cursor.execute(
        "INSERT INTO movies (title, genre, description, video_url) VALUES (?, ?, ?, ?)",
        (title, genre, desc, url)
    )

conn.commit()
conn.close()

print("🔥 Sample movies inserted successfully!")
