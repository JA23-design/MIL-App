from functools import wraps
from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from extensions import db
from models import InstallationResource, PCSChecklistItem, VehicleRule

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin: abort(403)
        return fn(*args, **kwargs)
    return wrapped

@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template("admin.html", resources=InstallationResource.query.count(), checklist=PCSChecklistItem.query.count(), vehicles=VehicleRule.query.count())

@admin_bp.route("/resource/new", methods=["GET","POST"])
@admin_required
def new_resource():
    from models import Base
    bases=Base.query.order_by(Base.name).all()
    if request.method=="POST":
        r=InstallationResource(base_id=request.form.get("base_id",type=int),category=request.form["category"],title=request.form["title"],description=request.form.get("description"),url=request.form.get("url"),phone=request.form.get("phone"),source_url=request.form.get("source_url"),last_verified=request.form.get("last_verified"))
        db.session.add(r); db.session.commit(); flash("Installation resource added."); return redirect(url_for("admin.dashboard"))
    return render_template("admin_resource.html", bases=bases)
