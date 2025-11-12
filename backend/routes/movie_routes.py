from flask import Blueprint, jsonify, request
from backend.controllers.movie_controller import get_all_movies, search_movies

movie_bp = Blueprint('movie_bp', __name__)

@movie_bp.route('/all', methods=['GET'])
def all_movies():
    return get_all_movies()

@movie_bp.route('/search', methods=['GET'])
def search():
    return search_movies()
