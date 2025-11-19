# backend/app.py

from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.database.db_connection import init_db
from backend.routes.auth_routes import auth_bp
from backend.routes.movie_routes import movie_bp
from backend.routes.subscription_routes import sub_bp
from backend.routes.admin_routes import admin_bp
from backend.extensions import mail

app = Flask(
    __name__,
    static_folder="../frontend",
    template_folder="../frontend"
)

CORS(app)
app.config["SECRET_KEY"] = "secret_key"

# EMAIL CONFIG
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="yourgmail@gmail.com",
    MAIL_PASSWORD="your_app_password"
)

mail.init_app(app)

# DB INIT
init_db()

# REGISTER BLUEPRINTS
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(movie_bp, url_prefix="/movies")
app.register_blueprint(sub_bp, url_prefix="/subscriptions")
app.register_blueprint(admin_bp, url_prefix="/admin")

# FRONTEND
@app.route("/")
def home_page():
    return send_from_directory("../frontend", "index.html")

@app.route("/login")
def login_page():
    return send_from_directory("../frontend", "login.html")

@app.route("/register")
def register_page():
    return send_from_directory("../frontend", "register.html")

@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    return send_from_directory("../frontend", "movie_detail.html")

@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory("../frontend/assets", filename)

@app.route("/<path:filename>")
def fallback(filename):
    return send_from_directory("../frontend", filename)

if __name__ == "__main__":
    app.run(debug=True)
