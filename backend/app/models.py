from datetime import UTC, datetime

from flask_security.models import sqla
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Model(DeclarativeBase):
    pass


sqla.FsModels.set_db_info(base_model=Model)


class Role(Model, sqla.FsRoleMixin):
    __tablename__ = "role"


class User(Model, sqla.FsUserMixin):
    __tablename__ = "user"
    notes: Mapped[list["Note"]] = relationship(back_populates="user")


class Note(Model):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="notes")
