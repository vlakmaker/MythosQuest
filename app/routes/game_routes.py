from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session, Response
from app.ai import stream_response

game_bp = Blueprint("game", __name__)

@game_bp.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("index.html", username=session["user"])

@game_bp.route("/generate", methods=["POST"])
def generate_response():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    return Response(stream_response(prompt), content_type='text/plain')
