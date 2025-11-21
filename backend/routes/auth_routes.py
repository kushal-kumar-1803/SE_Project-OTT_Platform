from flask import Blueprint
from backend.controllers.auth_controller import (
    register_user,
    login_user,
    forgot_password,
    reset_password
)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user()

@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user()

@auth_bp.route("/forgot_password", methods=["POST"])
def fp():
    return forgot_password()

@auth_bp.route("/reset_password", methods=["POST"])
def rp():
    return reset_password()
