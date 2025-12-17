# app/schemes/messages.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ==================== ОСНОВНЫЕ СХЕМЫ ====================

class SMessageGet(BaseModel):
    """Схема для получения сообщения"""
    id: int
    text: str
    sender_id: int
    recipient_id: int  # ← Исправлено с receiver_id
    is_read: bool = False
    created_at: datetime
    item_id: int  # ← Добавлено

    class Config:
        from_attributes = True


class SMessageGetWithRels(SMessageGet):
    """Схема сообщения с отношениями"""
    sender: Optional[dict] = None
    recipient: Optional[dict] = None
    item: Optional[dict] = None


# ==================== ДЛЯ API ====================

class SMessageAdd(BaseModel):
    """Схема для добавления ПРЯМОГО сообщения"""
    text: str
    recipient_id: int  # ← Исправлено: receiver_id → recipient_id
    item_id: int  # ← Обязательно! К какому товару сообщение?


SMessageCreate = SMessageAdd  # Алиас для совместимости


class SMessageUpdate(BaseModel):
    """Схема для обновления сообщения"""
    text: Optional[str] = None
    is_read: Optional[bool] = None


class SMessagePatch(BaseModel):
    """Схема для частичного обновления сообщения"""
    text: Optional[str] = None
    is_read: Optional[bool] = None


# ==================== ДЛЯ БУДУЩИХ ЧАТОВ ====================
# (пока не используем, оставляем для совместимости)

class SConversationGet(BaseModel):
    """Схема для получения чата (заглушка)"""
    id: int
    partner_name: str
    last_message: str
    unread_count: int = 0
    last_message_time: str


class SConversationList(BaseModel):
    """Схема для списка чатов (заглушка)"""
    id: int
    partner: str
    last_message: str
    unread: int
    time: str