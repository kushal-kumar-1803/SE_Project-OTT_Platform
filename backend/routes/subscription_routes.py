from flask import Blueprint
from backend.controllers.subscription_controller import subscribe_user, get_subscriptions

sub_bp = Blueprint('sub_bp', __name__)

@sub_bp.route('/add', methods=['POST'])
def add_subscription():
    return subscribe_user()

@sub_bp.route('/all', methods=['GET'])
def all_subscriptions():
    return get_subscriptions()
