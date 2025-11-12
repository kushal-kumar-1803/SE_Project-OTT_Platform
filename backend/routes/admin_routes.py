from flask import Blueprint
from backend.controllers.admin_controller import add_movie, update_movie, delete_movie, get_all_movies_admin

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/add', methods=['POST'])
def add_movie_route():
    return add_movie()

@admin_bp.route('/update/<int:movie_id>', methods=['PUT'])
def update_movie_route(movie_id):
    return update_movie(movie_id)

@admin_bp.route('/delete/<int:movie_id>', methods=['DELETE'])
def delete_movie_route(movie_id):
    return delete_movie(movie_id)

@admin_bp.route('/all', methods=['GET'])
def get_all_movies_route():
    return get_all_movies_admin()
