from flask import Blueprint, render_template, request
from models import ChildcareCenter

childcare_bp = Blueprint("childcare", __name__)

@childcare_bp.route("/childcare")
def childcare():
    base_id = request.args.get("base_id")

    query = ChildcareCenter.query

    if base_id:
        query = query.filter_by(base_id=base_id)

    centers = query.all()

    return render_template("childcare.html", centers=centers)
