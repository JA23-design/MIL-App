from flask import Blueprint, render_template, request
from flask_login import login_required
from extensions import db
from models import Base, InstallationResource

installations_bp = Blueprint("installations", __name__, url_prefix="/installations")

@installations_bp.route("/")
@login_required
def hub():
    bases = Base.query.order_by(Base.name).all()
    base_id = request.args.get("base_id", type=int)
    category = request.args.get("category", "")
    base = db.session.get(Base, base_id) if base_id else None
    resources = InstallationResource.query.filter_by(base_id=base_id).all() if base_id else []
    if category: resources = [r for r in resources if r.category == category]
    categories = sorted({r.category for r in resources})
    return render_template("installations.html", bases=bases, base=base, resources=resources, categories=categories, selected_category=category)
