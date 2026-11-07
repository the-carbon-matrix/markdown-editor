import os
import shutil

from flask import Blueprint, current_app, request
from flask_security import auth_required, current_user, roles_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import Note, User

user_bp = Blueprint("user", __name__)


@user_bp.route("/<id>/get_user", methods=["GET"])
@auth_required()
def get_user(id):
    if (current_user.id != int(id)) and (not current_user.has_role("admin")):
        return "You are not this user", 401
    else:
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


@user_bp.route("/create_note", methods=["POST"])
@roles_required("editor")
def create_note():
    data = request.json
    title = data.get("title")
    content = data.get("content")
    user_id = current_user.id

    folder = os.path.join(current_app.config["NOTES_DIR"], str(user_id))
    file_path = os.path.join(folder, secure_filename(f"{title}.md"))
    os.makedirs(folder, exist_ok=True)

    file_exists = os.path.exists(file_path)
    db_query = (
        db.session.query(Note)
        .filter(Note.title == title)
        .filter(Note.user_id == user_id)
    )
    db_entry_exists = db_query.first() is not None
    if file_exists and db_entry_exists:
        return "File already exists.", 409

    with open(file_path, "w") as f:
        # Note: If for whatever reason a file of the given name exists without a DB entry, it will just be overwritten
        f.write(content)

    new_note = Note(title=title, user_id=user_id, file_path=file_path)
    try:
        if db_entry_exists and (not file_exists):
            # Someone was messing with the data files, delete the previous DB entry and allow for the creation of a new one
            db_query.delete()
        db.session.add(new_note)
        db.session.commit()
        return str(new_note.id), 201
    except SQLAlchemyError as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.rollback()
        return str(e), 500


@user_bp.route("/get_note/<id>", methods=["GET"])
@auth_required()
def get_note(id):
    db_query = db.session.query(Note).filter(Note.id == id)
    db_entry = db_query.first()

    if db_entry is None:
        return "Note not found.", 404
    elif (db_entry.user_id != current_user.id) and (not current_user.has_role("admin")):
        return "This note isn't yours.", 401
    else:
        file_path = db_entry.file_path
        if not os.path.exists(file_path):
            # Someone was messing with the data files, delete the DB entry and send a 404
            try:
                db_query.delete()
                db.session.commit()
                return "Note not found.", 404
            except SQLAlchemyError as e:
                # Make sure the file is blank
                with open(file_path, "w") as f:
                    f.write("")
                db.session.rollback()
                return str(e), 500

        content = ""
        with open(file_path, "r") as f:
            content = f.read()

        return {
            "id": id,
            "user_id": current_user.id,
            "title": db_entry.title,
            "content": content,
        }


@user_bp.route("/<user_id>/get_all_notes", methods=["GET"])
@auth_required()
def get_all_notes(user_id):
    if (current_user.id != int(user_id)) and (not current_user.has_role("admin")):
        return "Forbidden", 401

    db_query = db.session.query(Note).filter(Note.user_id == user_id)
    notes = db_query.all()
    output = []
    try:
        for note in notes:
            # Delete the invalid notes whose file doesn't exist
            if not os.path.exists(note.file_path):
                db_query.filter(Note.id == note.id).delete()
            else:
                output.append({"id": note.id, "title": note.title})

        db.session.commit()
        return output

    except SQLAlchemyError as e:
        db.session.rollback()
        return str(e), 500


@user_bp.route("/edit_note/<id>", methods=["PATCH"])
@roles_required("editor")
def edit_note(id):
    data = request.json
    db_query = db.session.query(Note).filter(Note.id == id)
    db_entry = db_query.first()

    if db_entry is None:
        return "Note not found.", 404
    elif db_entry.user_id != current_user.id:
        return "This note isn't yours.", 401
    else:
        file_path = db_entry.file_path
        try:
            # Someone was messing with data files and the note doesn't exist
            if not os.path.exists(file_path):
                db_query.delete()
                db.session.commit()
                return "Note not found.", 404

            title = data.get("title")
            content = data.get("content")

            uniq = (
                db.session.query(Note)
                .filter(Note.title == title)
                .filter(Note.user_id == current_user.id)
                .first()
                is None
            )

            if not uniq:
                return "File already exists.", 409

            if title and uniq:
                folder = os.path.join(
                    current_app.config["NOTES_DIR"], str(current_user.id)
                )
                new_file_path = os.path.join(folder, secure_filename(f"{title}.md"))
                shutil.move(file_path, new_file_path)

                db_query.update({"title": title, "file_path": new_file_path})
                db.session.commit()

            if content:
                with open(file_path, "w") as f:
                    f.write(content)

            return id
        except SQLAlchemyError as e:
            db.session.rollback()
            return str(e), 500


@user_bp.route("/delete_note/<id>", methods=["DELETE"])
@auth_required()
def delete_note(id):
    db_query = db.session.query(Note).filter(Note.id == id)
    db_entry = db_query.first()

    if db_entry is None:
        return "Note not found.", 404
    elif (db_entry.user_id != current_user.id) and (not current_user.has_role("admin")):
        return "This note isn't yours.", 401
    else:
        file_path = db_entry.file_path
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            db_query.delete()
            db.session.commit()
            return id
        except SQLAlchemyError as e:
            # Make sure the file is blank
            with open(file_path, "w") as f:
                f.write("")
            db.session.rollback()
            return str(e), 500
