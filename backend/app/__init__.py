from flask import Flask
from .config import Config
from .extensions import db, jwt, bcrypt
from .auth import auth_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    CORS(app)

    # 👇 IMPORTANT: register blueprints
    app.register_blueprint(auth_bp)

    # 👇 IMPORTANT: import models so SQLAlchemy sees them
    with app.app_context():
        from . import models
        db.create_all()

    @app.route("/", methods=["GET"])
    def health_check():
        return {
            "status": "running",
            "service": "EduSphere Backend"
        }


    return app
