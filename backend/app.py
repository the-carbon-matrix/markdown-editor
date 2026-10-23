import os

from dotenv import load_dotenv
from flask_security.utils import hash_password

from app import create_app
from app.models import Model
from app.extensions import db, security

load_dotenv()
app = create_app()
with app.app_context():
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    admin_password = hash_password(os.environ.get("ADMIN_PASSWORD", "password"))

    Model.metadata.create_all(db.engine)

    editor_role = security.datastore.find_or_create_role("editor")
    admin_role = security.datastore.find_or_create_role("admin")

    if not security.datastore.find_user(email=admin_email):
        admin = security.datastore.create_user(
            name="Admin",
            username="admin",
            email=admin_email,
            password=admin_password,
        )
        security.datastore.add_role_to_user(admin, admin_role)
    security.datastore.commit()

if __name__ == "__main__":
    app.run()
