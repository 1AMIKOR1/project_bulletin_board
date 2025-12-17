# app/models/categories.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.database import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .items import ItemModel

class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # ДОБАВЬТЕ ЭТО ПОЛЕ:
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,  # Разрешить NULL
        default=None    # Значение по умолчанию
    )

    # Связь с товарами
    items: Mapped[list["ItemModel"]] = relationship("ItemModel", back_populates="category")