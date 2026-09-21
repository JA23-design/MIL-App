from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from extensions import db
from matcher import rank_providers
from models import Base, ChildcareCenter, MedicalProvider

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
@login_required
def search_page():
    bases = Base.query.order_by(Base.name).all()
    return render_template("search.html", bases=bases)


@search_bp.route("/api/search/bases")
@login_required
def api_bases():
    q = request.args.get("q", "").strip()
    results = Base.query.filter(Base.name.ilike(f"%{q}%")).order_by(Base.name).all()
    return jsonify([{"id": base.id, "name": base.name, "state": base.state} for base in results])


@search_bp.route("/results")
@login_required
def results():
    base_id = request.args.get("base_id", type=int)
    if not base_id:
        return render_template("results.html", providers=[], childcare=[], base=None)

    base = db.session.get(Base, base_id)
    if base is None:
        return render_template("results.html", providers=[], childcare=[], base=None)

    providers = MedicalProvider.query.filter_by(base_id=base.id).all()
    childcare = ChildcareCenter.query.filter_by(base_id=base.id).all()
    return render_template(
        "results.html",
        providers=rank_providers(providers),
        childcare=childcare,
        base=base,
    )
