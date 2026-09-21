from flask import Blueprint, render_template, request
from flask_login import login_required

from models import VehicleRule

vehicles_bp = Blueprint("vehicles", __name__, url_prefix="/vehicles")

STATES = [
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
    "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
    "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
    "TX","UT","VT","VA","WA","WV","WI","WY"
]

@vehicles_bp.route("/")
@login_required
def vehicles():
    state = request.args.get("state", "NC").upper()
    military_status = request.args.get("military_status", "Active-duty service member")
    if state not in STATES:
        state = "NC"

    rules = VehicleRule.query.filter_by(state=state).order_by(VehicleRule.benefit_type, VehicleRule.title).all()
    return render_template(
        "vehicles.html",
        states=STATES,
        selected_state=state,
        selected_military_status=military_status,
        rules=rules,
    )

