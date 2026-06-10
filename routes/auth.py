from flask import Blueprint, render_template, request, redirect
from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            email=request.form["email"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@auth_bp.route("/login")
def login():
    return render_template("login.html")
