import os

from flask import Blueprint, current_app, request
from flask_security import auth_required, current_user, roles_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import Note

user_bp = Blueprint("user", __name__)


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
    db_query = db.session.query(Note).filter(Note.title == title)
    db_entry_exists = db_query.first() is not None
    if file_exists and db_entry_exists:
        return "File already exists.", 409

    with open(file_path, "w") as f:
        # Note: If for whatever reason a file of the given name exists without a DB entry, it will just be overwritten
        f.write(content)

    new_note = Note(title=title, user_id=user_id, file_path=file_path)
    try:
        if db_entry_exists and (not file_exists):
            # Someone was messing with the static files, delete the previous DB entry and allow for the creation of a new one
            db_query.delete()
        db.session.add(new_note)
        db.session.commit()
        return str(new_note.id), 201
    except SQLAlchemyError as e:
        if os.path.exists(file_path):
            os.remove(file_path)
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
