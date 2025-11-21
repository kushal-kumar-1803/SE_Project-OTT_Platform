from flask import Blueprint, request, jsonify
from backend.services.log_service import LogService

logs_bp = Blueprint("logs_bp", __name__)

@logs_bp.route("/action", methods=["POST"])
def log_action():
    data = request.get_json()
    user_id = data.get("user_id")
    action = data.get("action")
    result = LogService.log_user_action(user_id, action)
    return jsonify(result)

@logs_bp.route("/error", methods=["POST"])
def log_error():
    data = request.get_json()
    error_msg = data.get("error")
    result = LogService.log_error(error_msg)
    return jsonify(result)
