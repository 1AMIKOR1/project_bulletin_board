# app/schemes/users.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
import re


# ==================== ОСНОВНЫЕ СХЕМЫ ====================

class UserBase(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr
    name: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_verified: bool = False
    image_id: Optional[int] = None


class User(UserBase):
    """Основная схема пользователя (для БД)"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== АВТОРИЗАЦИЯ ====================

class SUserAuth(BaseModel):
    """Для входа"""
    email: EmailStr
    password: str


class SUserAddRequest(BaseModel):
    """Для регистрации (запрос от клиента)"""
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None


    # @field_validator("password")
    # @classmethod
    # def validate_password(cls, v):
    #     if len(v) < 8:
    #         from pydantic import ValidationError
    #         raise ValidationError("Пароль должен содержать не менее 8 символов")
    #     if not re.search(r"[A-Z]", v):
    #         from pydantic import ValidationError
    #         raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
    #     if not re.search(r"[a-z]", v):
    #         from pydantic import ValidationError
    #         raise ValidationError("Пароль должен содержать хотя бы одну строчную букву")
    #     if not re.search(r"\d", v):
    #         from pydantic import ValidationError
    #         raise ValidationError("Пароль должен содержать хотя бы одну цифру")
    #     return v


class SUserAdd(BaseModel):
    """Для добавления в БД"""
    email: EmailStr
    hashed_password: str
    name: str
    phone: Optional[str] = None
    role_id: int | None = 1


# ==================== ДЛЯ API ====================

class SUserGet(BaseModel):
    """Для ответов API"""
    id: int
    name: str = ""
    email: str
    # trust_score: float = 5.0  # добавьте это поле
    hashed_password: str
    created_at: Optional[datetime] = None


class SUserResponse(BaseModel):
    """Для фронтенда"""
    id: int
    name: str = ""
    email: str
    trust_score: float


class SUserUpdate(BaseModel):
    """Для обновления"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_verified: Optional[bool] = None


class SUserPatch(BaseModel):
    """Для частичного обновления"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_verified: Optional[bool] = None


class SUserWithOffers(BaseModel):
    """Пользователь с предложениями"""
    user: SUserGet
    offers: list = []


# ==================== АЛИАСЫ ДЛЯ СОВМЕСТИМОСТИ ====================
# Создаем алиасы для существующего кода
# SUserGetWithRels = User  # временно, позже исправим