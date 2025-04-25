# app/__init__.py

from flask import Flask
from config import Config  # Adjust as needed for your config
from .models import db_session  # Make sure this path is correct

# Import your blueprints
from .routes.auth_routes import auth_bp
from .routes.game_routes import game_bp
from .routes.settings_routes import settings_bp
from .routes.home_routes import home_bp  # New redirect blueprint

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- Clean DB session teardown ---
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # --- Register blueprints ---
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(game_bp, url_prefix='/')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(home_bp)  # Handles bare "/"

    print("App created and blueprints registered.")
    print(f"Registered blueprints: {list(app.blueprints.keys())}")

    return app
