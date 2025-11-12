from flask import Flask
from flask_cors import CORS
from backend.database.db_connection import init_db
from backend.routes.auth_routes import auth_bp
from backend.routes.movie_routes import movie_bp
from backend.routes.subscription_routes import sub_bp
from backend.routes.admin_routes import admin_bp
from backend.controllers.logs_controller import logs_bp
from backend.controllers.instance_controller import instance_bp

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_jwt_secret_key'

# Initialize DB
init_db()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(movie_bp, url_prefix='/movies')
app.register_blueprint(sub_bp, url_prefix='/subscriptions')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(logs_bp, url_prefix='/logs')
app.register_blueprint(instance_bp, url_prefix='/instance')

@app.route('/')
def home():
    return {"message": "Welcome to the OTT Streaming Platform API!"}

if __name__ == '__main__':
    app.run(debug=True)
