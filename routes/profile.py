from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from extensions import db
from models import Base, FamilyProfile

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    bases = Base.query.order_by(Base.name).all()
    profile = FamilyProfile.query.filter_by(user_id=current_user.id).first()

    if request.method == "POST":
        if profile is None:
            profile = FamilyProfile(user_id=current_user.id)
            db.session.add(profile)

        base_id = request.form.get("base_id")
        profile.base_id = int(base_id) if base_id else None
        profile.has_children = "has_children" in request.form
        profile.child_age_range = request.form.get("child_age_range")
        profile.spouse_needs_healthcare = "spouse_needs" in request.form
        profile.destination_base_id = request.form.get("destination_base_id", type=int) or None
        profile.move_type = request.form.get("move_type", profile.move_type or "CONUS")
        profile.has_vehicle = "has_vehicle" in request.form
        profile.owns_or_rents_home = request.form.get("housing", profile.owns_or_rents_home or "Rent")
        profile.has_professional_license = "has_license" in request.form
        profile.has_pets = "has_pets" in request.form
        profile.pay_grade = request.form.get("pay_grade", "E-5")
        profile.with_dependents = "with_dependents" in request.form

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("profile.html", profile=profile, bases=bases)

