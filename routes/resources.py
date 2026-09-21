from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from extensions import db
from matcher import rank_providers
from models import Base, ChildcareCenter, FamilyProfile, MedicalProvider, CredentialRule

resources_bp = Blueprint("resources", __name__)


def current_base():
    profile = FamilyProfile.query.filter_by(user_id=current_user.id).first()
    base = db.session.get(Base, profile.base_id) if profile and profile.base_id else None
    return profile, base


@resources_bp.route("/healthcare")
@login_required
def healthcare():
    profile, base = current_base()
    providers = rank_providers(MedicalProvider.query.filter_by(base_id=base.id).all()) if base else []
    return render_template("healthcare.html", base=base, providers=providers, profile=profile)


@resources_bp.route("/childcare")
@login_required
def childcare():
    profile, base = current_base()
    centers = ChildcareCenter.query.filter_by(base_id=base.id).all() if base else []
    return render_template("childcare.html", base=base, centers=centers, profile=profile)


@resources_bp.route("/deers")
@login_required
def deers():
    return render_template("deers.html")


@resources_bp.route("/pcs")
@login_required
def pcs():
    return render_template("pcs.html")


@resources_bp.route("/credentials")
@login_required
def credentials():
    professions = ["Real Estate / Realtor", "Cosmetology", "Barber", "Esthetician", "Nail Technician", "Nursing", "Teaching", "Social Work", "Massage Therapy", "Childcare"]
    states = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    rules = []
    profession = request.args.get("profession", "")
    origin = request.args.get("origin", "")
    destination = request.args.get("destination", "")
    if profession and origin and destination:
        rules = CredentialRule.query.filter_by(profession=profession, origin_state=origin, destination_state=destination).all()
    return render_template("credentials.html", professions=professions, states=states, rules=rules, selected_profession=profession, selected_origin=origin, selected_destination=destination)

