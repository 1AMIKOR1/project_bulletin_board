# app/schemes/users.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
import re

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
