from flask import Flask
from flask_security import SQLAlchemyUserDatastore, user_registered

from .models import User


def setup_signals(app: Flask, user_datastore: SQLAlchemyUserDatastore):
    @user_registered.connect_via(app)
    def on_register(_, user: User, **_extra):
        user_datastore.add_role_to_user(user, "editor")
        user_datastore.deactivate_user(user)
