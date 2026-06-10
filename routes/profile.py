from flask import Blueprint, render_template, request
from models import FamilyProfile
from extensions import db

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        profile = FamilyProfile(
            user_id=1,  # placeholder for login user
            has_children="has_children" in request.form,
            child_age_range=request.form.get("child_age_range"),
            spouse_needs_healthcare="spouse_needs" in request.form
        )

        db.session.add(profile)
        db.session.commit()

    return render_template("profile.html")
