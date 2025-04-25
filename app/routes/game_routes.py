# game_routes.py

from flask import (
    Blueprint, render_template, redirect, url_for,
    request, jsonify, session, Response, stream_with_context # <<<--- Added stream_with_context
)
from app.stream_response import stream_response # Import the function that generates the stream content

# Define the blueprint for game-related routes
game_bp = Blueprint("game", __name__)

@game_bp.route("/")
def index():
    """
    Main game view. Only accessible to logged-in users.
    Checks session before rendering the main page.
    """
    # Check if the user is logged in by looking for 'user' in the session
    if "user" not in session:
        # If not logged in, redirect to the login page
        return redirect(url_for("auth.login"))
    # If logged in, render the main game page, passing the username
    return render_template("index.html", username=session["user"])

@game_bp.route("/generate", methods=["POST"])
def generate_response():
    """
    Handles prompt submission and streams the AI's response.
    Requires active session and uses stream_with_context.
    """
    # Verify user is logged in before proceeding
    if "user" not in session:
        # Return an error response if the user is not authenticated
        return jsonify({"error": "Unauthorized"}), 403 # Use 403 Forbidden for authenticated access failure

    # Expecting JSON data in the POST request
    data = request.json
    if not data:
        # Handle cases where request body is not JSON or empty
        return jsonify({"error": "Invalid request format, JSON expected"}), 400

    # Extract the prompt from the JSON data, default to empty string and strip whitespace
    prompt = data.get("prompt", "").strip()

    # Validate that the prompt is not empty
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # --- Refactoring for Streaming ---
    # Define an inner generator function. This function will be wrapped
    # by stream_with_context to keep the request context alive.
    def generate():
        # Delegate the actual generation logic (including context-sensitive
        # operations like get_current_user performed *before* the first yield
        # within stream_response) to the stream_response generator.
        yield from stream_response(prompt)

    # Return a Flask Response object.
    # Crucially, wrap the call to our inner generator `generate()`
    # with `stream_with_context`. This ensures that 'session' and other
    # request-specific objects remain accessible inside `stream_response`
    # even as chunks are yielded over time.
    # Set the content type to 'text/plain' for the streamed text data.
    return Response(stream_with_context(generate()), content_type="text/plain")
    # --- End Refactoring ---

@game_bp.route("/logout")
def logout():
    """
    Logs the user out by clearing the session.
    """
    # Clear all data stored in the session
    session.clear()
    # Redirect the user to the login page
    return redirect(url_for("auth.login"))