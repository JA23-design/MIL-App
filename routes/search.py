from flask import Blueprint, render_template, request, jsonify
from models import Base, MedicalProvider, ChildcareCenter
from matcher import rank_providers

search_bp = Blueprint("search", __name__)

@search_bp.route("/search")
def search_page():
    bases = Base.query.all()
    return render_template("search.html", bases=bases)


@search_bp.route("/api/search/bases")
def api_bases():
    q = request.args.get("q", "")

    results = Base.query.filter(Base.name.ilike(f"%{q}%")).all()

    return jsonify([
        {"id": b.id, "name": b.name, "state": b.state}
        for b in results
    ])


@search_bp.route("/results")
def results():
    base_id = request.args.get("base_id")

    providers = MedicalProvider.query.filter_by(base_id=base_id).all()
    childcare = ChildcareCenter.query.filter_by(base_id=base_id).all()

    ranked_providers = rank_providers(providers)

    return render_template(
        "results.html",
        providers=ranked_providers,
        childcare=childcare
    )
