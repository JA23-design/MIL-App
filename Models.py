from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_login import UserMixin

db = SQLAlchemy()

class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    branch = db.Column(db.String(50))

class MedicalProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"))
    tricare_prime = db.Column(db.Boolean, default=False)
    tricare_select = db.Column(db.Boolean, default=False)
    pediatric = db.Column(db.Boolean, default=False)
    vaccine_policy = db.Column(db.String(120))

class ChildcareCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"))
    accepts_ccys = db.Column(db.Boolean, default=False)
    age_range = db.Column(db.String(50))
    availability_status = db.Column(db.String(50))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))

class FamilyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    base_id = db.Column(db.Integer, db.ForeignKey("base.id"))

    has_children = db.Column(db.Boolean, default=False)
    child_age_range = db.Column(db.String(50))
    spouse_needs_healthcare = db.Column(db.Boolean, default=True)
