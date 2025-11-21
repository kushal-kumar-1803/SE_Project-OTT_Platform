from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.database.db_connection import init_db
from backend.routes.auth_routes import auth_bp
from backend.routes.movie_routes import movie_bp
from backend.routes.subscription_routes import sub_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.payment_routes import payment_bp
from backend.routes.profile_routes import profiles_bp
from backend.extensions import mail

# ----------------------------
# Flask App Config
# ----------------------------
app = Flask(
    __name__,
    static_folder="../frontend/assets",
    template_folder="../frontend"
)

CORS(app)
app.config["SECRET_KEY"] = "secret_key"

# EMAIL CONFIG (optional - used for password reset / notifications)
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="mdsadatullah97@gmail.com",
    MAIL_PASSWORD="gagy oayf vtrv upvz"
)

mail.init_app(app)

# Init DB
init_db()

# APIs
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(movie_bp, url_prefix="/movies")
app.register_blueprint(sub_bp, url_prefix="/subscriptions")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(payment_bp, url_prefix="/payments")
app.register_blueprint(profiles_bp, url_prefix="/profiles")

# -----------------------------
# FRONTEND ROUTES
# -----------------------------
@app.route("/")
def home_page():
    return send_from_directory("../frontend", "index.html")


@app.route("/login")
def login_page():
    return send_from_directory("../frontend", "login.html")


@app.route("/register")
def register_page():
    return send_from_directory("../frontend", "register.html")


@app.route("/forgot")
def forgot_page():
    return send_from_directory("../frontend", "forgot.html")


@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    return send_from_directory("../frontend", "movie_detail.html")


# Admin frontend pages
@app.route("/admin")
def admin_page():
    return send_from_directory("../frontend", "admin_panel.html")


@app.route("/admin/login")
def admin_login_page():
    return send_from_directory("../frontend", "admin_login.html")


# PROFILE FRONTEND ROUTES
@app.route("/profiles")
def profiles_page():
    return send_from_directory("../frontend", "profile.html")


@app.route("/profiles/create")
def profiles_create_page():
    return send_from_directory("../frontend", "profile_create.html")


@app.route("/profiles/manage")
def profiles_manage_page():
    return send_from_directory("../frontend", "profile_manage.html")


# Static (CSS, JS, images)
@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("../frontend/assets", path)


# Subscribe / Payment pages
@app.route("/subscribe")
def subscribe_page():
    return send_from_directory("../frontend", "subscribe.html")


@app.route("/payment")
def payment_page():
    return send_from_directory("../frontend", "payment.html")


if __name__ == "__main__":
    app.run(debug=True)
from flask import send_from_directory

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('../frontend/videos', filename)
if __name__ == "__main__":
    app.run()
