from datetime import UTC, datetime

from flask_security.models import fsqla_v4 as fsqla
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db

fsqla.FsModels.set_db_info(db)  # pyright: ignore[reportPrivateImportUsage]


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"


class FsRefreshTracker(db.Model, fsqla.FsRefreshTrackerMixin):
    __tablename__ = "refresh_tracker"


class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = "user"
    notes: Mapped[list["Note"]] = relationship(back_populates="user")


class Note(db.Model):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    modified_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="notes")

    __table_args__ = (UniqueConstraint("title", "user_id", name="uq_user_note_title"),)
