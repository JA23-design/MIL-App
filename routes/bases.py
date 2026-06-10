from flask import Blueprint, render_template
from models import db, Base

bases_bp = Blueprint("bases", __name__)

@bases_bp.route("/bases")
def bases():
    bases = Base.query.order_by(Base.name).all()
    return render_template("bases.html", bases=bases)
