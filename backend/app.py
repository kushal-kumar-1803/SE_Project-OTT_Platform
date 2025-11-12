from flask import Flask
from flask_cors import CORS
from backend.database.db_connection import init_db
from backend.routes.auth_routes import auth_bp
from backend.routes.movie_routes import movie_bp
from backend.routes.subscription_routes import sub_bp
from backend.routes.admin_routes import admin_bp


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

@app.route('/')
def home():
    return {"message": "Welcome to the OTT Streaming Platform API!"}

if __name__ == '__main__':
    app.run(debug=True)
