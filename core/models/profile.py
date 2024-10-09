from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base

from .mixins import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _user_back_populates = 'profile'
    _user_id_unique = True
    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None]
