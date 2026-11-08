import os
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_security import FSQLALiteUserDatastore

from .extensions import db, security
from .forms import ExtendedRegisterForm
from .models import Role, User
from .routes import main
from .signals import setup_signals


def create_app():
    app = Flask(__name__)

    BASE_DIR = Path(__file__).resolve().parent

    app.config["SECURITY_API_ENABLED_METHODS"] = ["token"]

    app.config["SQLALCHEMY_ENGINES"] = {
        "default": os.environ.get("SQLALCHEMY_DATABASE_URI")
    }
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT")
    app.config["SECURITY_REGISTERABLE"] = True
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False
    app.config["SECURITY_USE_REGISTER_V2"] = True

    app.config["SECURITY_USERNAME_ENABLE"] = True
    app.config["SECURITY_USERNAME_REQUIRED"] = True
    app.config["SECURITY_RECOVERABLE"] = False
    app.config["SECURITY_CHANGEABLE"] = False
    app.config["SECURITY_CONFIRMABLE"] = False

    app.config["NOTES_DIR"] = str(BASE_DIR / "data" / "notes")
    os.makedirs(app.config["NOTES_DIR"], exist_ok=True)

    db.init_app(app)
    user_datastore = FSQLALiteUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)

    app.register_blueprint(main)
    setup_signals(app, user_datastore)

    CORS(app, origins=[os.environ.get("FRONTEND_URL", "localhost:3000")])

    return app
