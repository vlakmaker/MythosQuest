from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash
)
from app.models import get_user, add_user, verify_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.")
            return redirect(url_for("auth.login"))

        if verify_user(username, password):
            session["user"] = username
            return redirect(url_for("game.index"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please fill in all fields.")
            return redirect(url_for("auth.register"))

        if get_user(username):
            flash("Username already taken.")
            return redirect(url_for("auth.register"))

        try:
            add_user(username, password)
            flash("Account created. Please log in.")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash("An error occurred while creating your account.")
            return redirect(url_for("auth.register"))

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
