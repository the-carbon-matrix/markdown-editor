from flask import Blueprint
from flask_security import auth_required, roles_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import User

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/activate_user/<id>", methods=["PATCH"])
@roles_required("admin")
@auth_required("token")
def enable_user(id):
    try:
        user_query = db.session.query(User).filter(User.id == id)
        user = user_query.first()
        if (not user) or (user.has_role("admin")):
            return {"error": "User not found."}, 404

        user_query.update({User.active: True})
        db.session.commit()
        return id
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


@admin_bp.route("/deactivate_user/<id>", methods=["PATCH"])
@roles_required("admin")
@auth_required("token")
def disable_user(id):
    try:
        user_query = db.session.query(User).filter(User.id == id)
        user = user_query.first()
        if (not user) or (user.has_role("admin")):
            return {"error": "User not found."}, 404

        user_query.update({User.active: False})
        db.session.commit()
        return id
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


@admin_bp.route("/get_all_users", methods=["GET"])
@roles_required("admin")
@auth_required("token")
def get_all_users():
    users = db.session.query(User).all()
    return [
        {
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "is_active": user.is_active,
            "created_at": user.create_datetime,
        }
        for user in users
    ]


@admin_bp.route("/get_user/<id>", methods=["GET"])
@roles_required("admin")
@auth_required("token")
def get_user(id):
    user = db.session.query(User).filter(User.id == id).first()
    if not user:
        return "User doesn't exist", 404
    return {
        "username": user.username,
        "email": user.email,
        "id": user.id,
        "is_active": user.is_active,
        "created_at": user.create_datetime,
    }


@admin_bp.route("/delete_user/<id>", methods=["DELETE"])
@roles_required("admin")
@auth_required("token")
def delete_user(id):
    try:
        user_query = db.session.query(User).filter(User.id == id)
        user = user_query.first()
        if (not user) or (user.has_role("admin")):
            return {"error": "User not found."}, 404

        user_query.delete()
        db.session.commit()
        return id
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500
