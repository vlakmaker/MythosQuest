from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import check_password_hash
from app.models import get_user, add_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = get_user(username)
        if user and check_password_hash(user[2], password):  # user[2] = hashed password
            session["user"] = user[1]  # user[1] = username
            return redirect(url_for("game.index"))
        else:
            return render_template("login.html", error="Invalid username or password")
    
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if not username or not password:
            return render_template("register.html", error="Please fill out all fields.")

        if get_user(username):
            return render_template("register.html", error="Username already exists.")

        add_user(username, password)
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
