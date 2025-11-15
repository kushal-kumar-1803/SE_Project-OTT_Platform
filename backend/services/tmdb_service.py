# backend/services/tmdb_service.py
import os
import requests

TMDB_KEY = os.getenv("TMDB_API_KEY") or "ec726bf0d6157607e751561eb4e9e097"
TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_BASE = "https://image.tmdb.org/t/p"

def _get(url, params=None):
    params = params or {}
    params["api_key"] = TMDB_KEY
    r = requests.get(f"{TMDB_BASE}{url}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def get_movie_detail(movie_id):
    """Return the TMDB movie detail JSON for given id."""
    return _get(f"/movie/{movie_id}", params={"language": "en-US"})

def search_movies(q, page=1):
    """Return search results from TMDB (movie search)."""
    return _get("/search/movie", params={"query": q, "page": page, "language":"en-US"})

def get_image_url(path, size="w500"):
    if not path:
        return None
    return f"{TMDB_IMG_BASE}/{size}{path}"
