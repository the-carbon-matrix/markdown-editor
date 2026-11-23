import os
import shutil

from flask import Blueprint, current_app
from flask_security import auth_required, roles_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import Note, User

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

        user_query.update({"active": True})
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

        user_query.update({"active": False})
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
        if user.has_role("editor")
    ]


@admin_bp.route("/get_all_notes", methods=["GET"])
@roles_required("admin")
@auth_required("token")
def get_all_notes():
    db_query = db.session.query(Note)
    notes = db_query.all()
    output = []
    try:
        for note in notes:
            # Delete the invalid notes whose file doesn't exist
            if not os.path.exists(note.file_path):
                db_query.filter(Note.id == note.id).delete()
            else:
                output.append(
                    {
                        "id": note.id,
                        "user_id": note.user_id,
                        "title": note.title,
                        "created_at": note.created_at,
                        "modified_at": note.modified_at,
                    }
                )

        db.session.commit()
        return output

    except SQLAlchemyError as e:
        db.session.rollback()
        return str(e), 500


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
def delete_user(id):
    try:
        user_query = db.session.query(User).filter(User.id == id)
        user = user_query.first()
        if (not user) or (user.has_role("admin")):
            return {"error": "User not found."}, 404

        db.session.query(Note).filter(Note.user_id == id).delete()
        folder = os.path.join(current_app.config["NOTES_DIR"], str(id))
        if os.path.exists(folder):
            shutil.rmtree(folder)

        user_query.delete()
        db.session.commit()
        return id
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500
