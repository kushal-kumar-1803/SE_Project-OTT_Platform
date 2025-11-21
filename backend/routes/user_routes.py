# backend/routes/user_routes.py
"""
User routes for watch history, watchlist, ratings, and profile management
Aligns with OTT-F-004 (View Profile), OTT-F-005 (Update Profile),
OTT-F-040 (Resume playback), OTT-F-050 (Subscriptions/Watchlist)
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
    get_user_rating,
    get_user_profile,
    update_user_profile
)

user_bp = Blueprint('user', __name__, url_prefix='/user')

# ===== PROFILE =====
user_bp.route('/profile', methods=['GET'])(get_user_profile)
user_bp.route('/profile', methods=['PUT'])(update_user_profile)

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

