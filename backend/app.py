from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.database.db_connection import init_db
from backend.routes.auth_routes import auth_bp
from backend.routes.movie_routes import movie_bp
from backend.routes.subscription_routes import sub_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.profile_routes import profiles_bp

app = Flask(
    __name__,
    static_folder="../frontend/assets",
    template_folder="../frontend"
)

CORS(app)
app.config["SECRET_KEY"] = "secret_key"

# Init DB
init_db()

# APIs
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(movie_bp, url_prefix="/movies")
app.register_blueprint(sub_bp, url_prefix="/subscriptions")
app.register_blueprint(admin_bp, url_prefix="/admin")
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

@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    return send_from_directory("../frontend", "movie_detail.html")

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


# IMPORTANT: REMOVE OLD FALLBACK (it was breaking /profiles)
# Do NOT add fallback route again.


if __name__ == "__main__":
    app.run(debug=True)
