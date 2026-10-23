import os

from flask import Flask
from flask_security import FSQLALiteUserDatastore

from .extensions import db, security
from .forms import ExtendedRegisterForm
from .models import Role, User
from .routes import main


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_ENGINES"] = {
        "default": os.environ.get("SQLALCHEMY_DATABASE_URI")
    }
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT")
    app.config["SECURITY_REGISTERABLE"] = True
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False
    app.config["SECURITY_USE_REGISTER_V2"] = True

    app.config["SECURITY_RECOVERABLE"] = True
    app.config["SECURITY_CHANGEABLE"] = True
    app.config["SECURITY_CONFIRMABLE"] = False
    app.config["SECURITY_LOGOUT_METHODS"] = ["GET", "POST"]

    db.init_app(app)
    user_datastore = FSQLALiteUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)

    app.register_blueprint(main)
    return app
