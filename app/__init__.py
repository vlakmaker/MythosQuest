from flask import Flask
from config import FLASK_SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.secret_key = FLASK_SECRET_KEY

    # Import and register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.game_routes import game_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)

    return app
