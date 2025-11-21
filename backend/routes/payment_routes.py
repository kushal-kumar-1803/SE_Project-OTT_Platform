from flask import Blueprint
from backend.controllers.payment_controller import (
    create_payment_request,
    get_pending_payments,
    approve_payment
)

payment_bp = Blueprint("payment_bp", __name__)

@payment_bp.route("/create", methods=["POST"])
def create():
    return create_payment_request()

@payment_bp.route("/pending")
def pending_payments():
    return get_pending_payments()

@payment_bp.route("/approve", methods=["POST"])
def approve():
    return approve_payment()
