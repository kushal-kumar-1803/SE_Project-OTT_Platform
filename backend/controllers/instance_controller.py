from flask import Blueprint, jsonify
from backend.services.instance_service import InstanceService

instance_bp = Blueprint("instance_bp", __name__)

@instance_bp.route("/status", methods=["GET"])
def instance_status():
    status = InstanceService.get_instance_status()
    return jsonify(status)
