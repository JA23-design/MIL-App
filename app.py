from flask import Flask, render_template
from config import Config
from extensions import db, login_manager

from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.search import search_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(search_bp)

    @app.route("/")
    def home():
        return render_template("dashboard.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
