from flask import Blueprint, redirect

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def index():
    return redirect("/auth/login")
