# app/__init__.py

from flask import Flask
from config import Config # Or however you import your config
# Import other necessary Flask extensions if you have them

# Import the scoped session object from your models file
from .models import db_session # <-- Make sure this import path is correct

# Import your blueprints
from .routes.auth_routes import auth_bp
from .routes.game_routes import game_bp
from .routes.settings_routes import settings_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- Add this section for Session Teardown ---
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """
        Removes the database session after each request.
        This ensures the session associated with the current application context
        (usually tied to the request thread) is properly closed and removed,
        preventing potential leaks or stale data issues.
        It's the responsibility of scoped_session's remove() method.
        """
        db_session.remove()
    # --- End Session Teardown section ---

    # Initialize other Flask extensions here (e.g., LoginManager, etc.)
    # ...

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth') # Example prefix, adjust if needed
    app.register_blueprint(game_bp, url_prefix='/')     # Assuming game is the root
    app.register_blueprint(settings_bp, url_prefix='/settings') # Example prefix

    # You might have other app setup logic here
    # ...

    print("App created and blueprints registered.") # Optional: for debugging startup
    print(f"Registered blueprints: {list(app.blueprints.keys())}")

    return app