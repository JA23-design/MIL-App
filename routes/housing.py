from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from extensions import db
from models import BAHRate, Base, FamilyProfile, HousingCommunity

housing_bp = Blueprint("housing", __name__, url_prefix="/housing")


@housing_bp.route("/")
@login_required
def housing():
    profile = FamilyProfile.query.filter_by(user_id=current_user.id).first()
    base_id = request.args.get("base_id", type=int) or (profile.base_id if profile else None)
    base = db.session.get(Base, base_id) if base_id else None

    communities = HousingCommunity.query.filter_by(base_id=base_id).order_by(HousingCommunity.name).all() if base_id else []
    bah_rates = BAHRate.query.filter_by(base_id=base_id).order_by(BAHRate.pay_grade).all() if base_id else []

    selected_grade = profile.pay_grade if profile else "E-5"
    selected_dependents = profile.with_dependents if profile else True
    selected_bah = next(
        (
            rate for rate in bah_rates
            if rate.pay_grade == selected_grade and rate.with_dependents == selected_dependents
        ),
        None,
    )

    return render_template(
        "housing.html",
        base=base,
        bases=Base.query.order_by(Base.name).all(),
        communities=communities,
        bah_rates=bah_rates,
        selected_grade=selected_grade,
        selected_dependents=selected_dependents,
        selected_bah=selected_bah,
    )
