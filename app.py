import os
from app import create_app
from models import db, Base, MedicalProvider, ChildcareCenter
from routes.search import search_bp

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Bases
    fort_liberty = Base(name="Fort Liberty", state="NC", city="Fayetteville", branch="Army")
    camp_lejeune = Base(name="Camp Lejeune", state="NC", city="Jacksonville", branch="Navy")

    db.session.add_all([fort_liberty, camp_lejeune])
    db.session.commit()

    # Medical providers
    db.session.add_all([
        MedicalProvider(name="Liberty Family Clinic", base_id=fort_liberty.id, tricare_prime=True, pediatric=True),
        MedicalProvider(name="Lejeune Health Center", base_id=camp_lejeune.id, tricare_select=True, pediatric=False),
    ])

    # Childcare
    db.session.add_all([
        ChildcareCenter(name="Liberty CDC", base_id=fort_liberty.id, accepts_ccys=True, age_range="0-5", availability_status="open"),
        ChildcareCenter(name="Lejeune Kids Care", base_id=camp_lejeune.id, accepts_ccys=True, age_range="0-12", availability_status="waitlist"),
    ])

    db.session.commit()

print("Database initialized.")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from routes.bases import bases_bp
    from routes.healthcare import healthcare_bp
    from routes.childcare import childcare_bp

    app.register_blueprint(bases_bp)
    app.register_blueprint(healthcare_bp)
    app.register_blueprint(childcare_bp)
    app.register_blueprint(search_bp)   # NEW

    @app.route("/")
    def home():
        return render_template("home.html")

    return app
