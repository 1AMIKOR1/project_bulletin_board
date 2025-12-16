# app/models/users.py
from os import name
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.database.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .items import ItemModel
    from .messages import MessageModel
    from .reviews import ReviewModel
    from .roles import RoleModel

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(300), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)

    # Связи — через TYPE_CHECKING
    role: Mapped["RoleModel"] = relationship("RoleModel", back_populates="users")
    items: Mapped[list["ItemModel"]] = relationship("ItemModel", back_populates="owner")
    reviews_as_author: Mapped[list["ReviewModel"]] = relationship(
        "ReviewModel", foreign_keys="ReviewModel.user_id", back_populates="author"
    )
    #reviews_as_recipient: Mapped[list["ReviewModel"]] = relationship(
       # "ReviewModel", foreign_keys="ReviewModel.item_id", back_populates="item"
    #)
    sent_messages: Mapped[list["MessageModel"]] = relationship(
        "MessageModel", foreign_keys="MessageModel.sender_id", back_populates="sender"
    )
    received_messages: Mapped[list["MessageModel"]] = relationship(
        "MessageModel", foreign_keys="MessageModel.recipient_id", back_populates="recipient"
    )