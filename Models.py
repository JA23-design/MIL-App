from flask_login import UserMixin
from extensions import db


class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    branch = db.Column(db.String(50), nullable=False)

    medical_providers = db.relationship("MedicalProvider", backref="base", lazy=True, cascade="all, delete-orphan")
    childcare_centers = db.relationship("ChildcareCenter", backref="base", lazy=True, cascade="all, delete-orphan")
    family_profiles = db.relationship("FamilyProfile", backref="base", lazy=True)
    housing_communities = db.relationship("HousingCommunity", backref="base", lazy=True, cascade="all, delete-orphan")
    bah_rates = db.relationship("BAHRate", backref="base", lazy=True, cascade="all, delete-orphan")
    installation_resources = db.relationship("InstallationResource", backref="base", lazy=True, cascade="all, delete-orphan")


class MedicalProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"), nullable=False)
    tricare_prime = db.Column(db.Boolean, default=False)
    tricare_select = db.Column(db.Boolean, default=False)
    pediatric = db.Column(db.Boolean, default=False)
    vaccine_policy = db.Column(db.String(120))
    category = db.Column(db.String(80), default="Clinic")


class ChildcareCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"), nullable=False)
    accepts_ccys = db.Column(db.Boolean, default=False)
    age_range = db.Column(db.String(50))
    availability_status = db.Column(db.String(50), default="Check availability")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    profile = db.relationship(
        "FamilyProfile",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class FamilyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"))
    has_children = db.Column(db.Boolean, default=False)
    child_age_range = db.Column(db.String(50))
    spouse_needs_healthcare = db.Column(db.Boolean, default=True)
    pay_grade = db.Column(db.String(10), default="E-5")
    with_dependents = db.Column(db.Boolean, default=True)
    destination_base_id = db.Column(db.Integer, db.ForeignKey("base.id"))
    move_type = db.Column(db.String(20), default="CONUS")
    has_vehicle = db.Column(db.Boolean, default=True)
    owns_or_rents_home = db.Column(db.String(30), default="Rent")
    has_professional_license = db.Column(db.Boolean, default=False)
    has_pets = db.Column(db.Boolean, default=False)


class HousingCommunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    bedrooms = db.Column(db.String(50))
    eligibility = db.Column(db.String(120))
    housing_type = db.Column(db.String(50), default="On-base")
    website = db.Column(db.String(500))


class BAHRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    pay_grade = db.Column(db.String(10), nullable=False)
    with_dependents = db.Column(db.Boolean, nullable=False)
    monthly_rate = db.Column(db.Integer, nullable=False)
    source_url = db.Column(db.String(500))


class CredentialRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.String(120), nullable=False)
    origin_state = db.Column(db.String(2), nullable=False)
    destination_state = db.Column(db.String(2), nullable=False)
    pathway = db.Column(db.String(120), nullable=False)
    documents = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    source_url = db.Column(db.String(500), nullable=False)
    last_verified = db.Column(db.String(20), nullable=False)


class VehicleRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), nullable=False)
    military_status = db.Column(db.String(80), nullable=False)
    benefit_type = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text, nullable=False)
    documents = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.String(500), nullable=False)
    last_verified = db.Column(db.String(20), nullable=False)


class InstallationResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500))
    phone = db.Column(db.String(80))
    source_url = db.Column(db.String(500))
    last_verified = db.Column(db.String(20))


class PCSChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    phase = db.Column(db.String(40), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    move_type = db.Column(db.String(20), default="ANY")
    requires_children = db.Column(db.Boolean, default=False)
    requires_vehicle = db.Column(db.Boolean, default=False)
    requires_license = db.Column(db.Boolean, default=False)
    requires_pets = db.Column(db.Boolean, default=False)
    source_url = db.Column(db.String(500))


class UserTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    checklist_item_id = db.Column(db.Integer, db.ForeignKey("pcs_checklist_item.id"))
    title = db.Column(db.String(180), nullable=False)
    phase = db.Column(db.String(40), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    user = db.relationship("User", backref=db.backref("tasks", lazy=True, cascade="all, delete-orphan"))
    checklist_item = db.relationship("PCSChecklistItem")

