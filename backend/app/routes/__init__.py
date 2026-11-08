from flask import Blueprint

from .admin import admin_bp
from .user import user_bp

main = Blueprint("main", __name__, url_prefix="/api")
main.register_blueprint(admin_bp, url_prefix="/admin")
main.register_blueprint(user_bp, url_prefix="/user")
