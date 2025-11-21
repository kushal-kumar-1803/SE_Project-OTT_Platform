# backend/routes/user_routes.py
"""
User routes for watch history, watchlist, ratings
Aligns with OTT-F-040 (Resume playback), OTT-F-050 (Subscriptions/Watchlist)
"""

from flask import Blueprint
from backend.controllers.user_controller import (
    add_to_watch_history,
    get_watch_history,
    get_resume_position,
    add_to_watchlist,
    remove_from_watchlist,
    get_watchlist,
    add_rating,
    get_movie_ratings,
    get_user_rating
)

user_bp = Blueprint('user', __name__, url_prefix='/user')

# ===== WATCH HISTORY =====
user_bp.route('/watch-history', methods=['POST'])(add_to_watch_history)
user_bp.route('/watch-history', methods=['GET'])(get_watch_history)
user_bp.route('/resume', methods=['GET'])(get_resume_position)

# ===== WATCHLIST =====
user_bp.route('/watchlist', methods=['POST'])(add_to_watchlist)
user_bp.route('/watchlist', methods=['DELETE'])(remove_from_watchlist)
user_bp.route('/watchlist', methods=['GET'])(get_watchlist)

# ===== RATINGS =====
user_bp.route('/rating', methods=['POST'])(add_rating)
user_bp.route('/movie-ratings', methods=['GET'])(get_movie_ratings)
user_bp.route('/rating', methods=['GET'])(get_user_rating)
