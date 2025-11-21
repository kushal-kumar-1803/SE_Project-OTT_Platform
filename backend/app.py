from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.database.db_connection import init_db
from backend.routes.auth_routes import auth_bp
from backend.routes.movie_routes import movie_bp
from backend.routes.subscription_routes import sub_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.user_routes import user_bp
from backend.extensions import mail

# Check if payment_routes exists, if so import it
try:
    from backend.routes.payment_routes import payment_bp
    has_payments = True
except ImportError:
    has_payments = False

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

# EMAIL CONFIG
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="mdsadatullah97@gmail.com",  # Your Gmail address
    MAIL_PASSWORD="gagy oayf vtrv upvz"  # Gmail App Password
)

mail.init_app(app)

# ----------------------------
# Initialize DB
# ----------------------------
init_db()

# ----------------------------
# Register API Blueprints
# ----------------------------
# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(movie_bp, url_prefix="/movies")
app.register_blueprint(sub_bp, url_prefix="/subscriptions")
app.register_blueprint(admin_bp, url_prefix="/admin-api")
app.register_blueprint(user_bp, url_prefix="/user")

if has_payments:
    app.register_blueprint(payment_bp, url_prefix="/payments")


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

@app.route("/admin")
def admin_page():
    return send_from_directory("../frontend", "admin_panel.html")

@app.route("/admin/login")
def admin_login_page():
    return send_from_directory("../frontend", "admin_login.html")


# -----------------------------
# STATIC FILES (CSS, JS, IMAGES)
# -----------------------------

@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("../frontend/assets", path)


# -----------------------------
# IMPORTANT!!
# THIS FALLBACK SHOULD NOT OVERRIDE API ROUTES
# -----------------------------
@app.route("/page/<path:filename>")
def fallback_html(filename):
    """
    Only serve HTML pages for user navigation.
    Prevents conflict with API routes.
    """
    try:
        return send_from_directory("../frontend", filename)
    except:
        return send_from_directory("../frontend", "index.html")
    
@app.route("/subscribe")
def subscribe_page():
    return send_from_directory("../frontend", "subscribe.html")

@app.route("/payment")
def payment_page():
    return send_from_directory("../frontend", "payment.html")




if __name__ == "__main__":
  app.run(debug=True)