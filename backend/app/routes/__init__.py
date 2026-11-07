from flask import Blueprint, render_template
from flask_security import auth_required, roles_accepted

from .admin import admin_bp
from .user import user_bp

main = Blueprint("main", __name__, url_prefix="/api")
main.register_blueprint(admin_bp, url_prefix="/admin")
main.register_blueprint(user_bp, url_prefix="/user")


@main.route("/")
@auth_required()
def index():
    return render_template("index.html")


@main.route("/admin")
@roles_accepted("admin")
def admin():
    return "<h1>Admin</h1>"
