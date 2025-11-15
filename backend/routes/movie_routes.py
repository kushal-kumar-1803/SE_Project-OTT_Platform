# backend/routes/movie_routes.py
from flask import Blueprint
from backend.controllers.movie_controller import (
    get_all_movies,
    search_local_movies,
    get_tmdb_movie,
    search_tmdb_movies
)

movie_bp = Blueprint('movie_bp', __name__)

# -------------------------
# LOCAL DB MOVIE ROUTES
# -------------------------

@movie_bp.route('/all', methods=['GET'])
def all_movies():
    return get_all_movies()


@movie_bp.route('/search', methods=['GET'])
def search():
    return search_local_movies()

# -------------------------
# TMDB MOVIE ROUTES
# -------------------------

@movie_bp.route('/tmdb/<int:movie_id>', methods=['GET'])
def tmdb_detail(movie_id):
    return get_tmdb_movie(movie_id)


@movie_bp.route('/tmdb_search', methods=['GET'])
def tmdb_search_route():
    return search_tmdb_movies()
