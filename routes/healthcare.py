from flask import Blueprint, render_template, request
from models import MedicalProvider

healthcare_bp = Blueprint("healthcare", __name__)

@healthcare_bp.route("/healthcare")
def healthcare():
    base_id = request.args.get("base_id")

    query = MedicalProvider.query

    if base_id:
        query = query.filter_by(base_id=base_id)

    providers = query.all()

    return render_template("healthcare.html", providers=providers)
