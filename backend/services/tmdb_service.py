# backend/services/tmdb_service.py

import requests

TMDB_API_KEY = "ec726bf0d6157607e751561eb4e9e097"
TMDB_BASE = "https://api.themoviedb.org/3"


def tmdb_get(url):
    r = requests.get(url)
    return r.json()


def get_image_url(path, size="original"):
    if not path:
        return None
    return f"https://image.tmdb.org/t/p/{size}{path}"


def search_movies(query):
    url = f"{TMDB_BASE}/search/movie?api_key={TMDB_API_KEY}&query={query}"
    return tmdb_get(url)


def get_movie_detail(movie_id):
    url = f"{TMDB_BASE}/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=videos"
    data = tmdb_get(url)
    return data


def get_movie_trailer(movie_id):
    """
    Returns the FIRST YouTube trailer
    """
    url = f"{TMDB_BASE}/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
    data = tmdb_get(url)

    videos = data.get("results", [])

    youtube_trailers = [
        v for v in videos
        if v.get("site") == "YouTube" and v.get("type") == "Trailer"
    ]

    if not youtube_trailers:
        return {"youtube_key": None}

    return {"youtube_key": youtube_trailers[0]["key"]}
