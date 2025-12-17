# app/api/messages.py
from fastapi import APIRouter, Depends
from typing import Optional
from app.exceptions.messages import (
    MessageNotFoundError,
    MessageNotFoundHTTPError,
    MessageAccessDeniedError,
    MessageAccessDeniedHTTPError
)
from app.schemes.messages import (
    SMessageAdd,
    SMessageGet,
    SConversationGet,  # Оставляем для будущего
    SConversationList  # Оставляем для будущего
)
from app.services.messages import MessageService
from app.api.dependencies import DBDep

router = APIRouter(prefix="/messages", tags=["Сообщения"])


# ==================== ПРЯМЫЕ СООБЩЕНИЯ ====================

@router.post("", summary="Отправить прямое сообщение")
async def send_message(
    db: DBDep,
    message_data: SMessageAdd,
    current_user_id: int = 1  # ← Временное решение! Потом из токена
) -> dict[str, str]:
    """
    Отправить сообщение другому пользователю.

    Временный параметр current_user_id - ID отправителя.
    В будущем будет извлекаться из JWT токена.
    """
    try:
        await MessageService(db).send_direct_message(
            message_data=message_data,
            current_user_id=current_user_id
        )
        return {"status": "OK", "message": "Сообщение отправлено"}
    except Exception as e:
        # Временная обработка ошибок
        return {"status": "ERROR", "detail": str(e)}


@router.get("", summary="Получить все сообщения (для админа)")
async def get_all_messages(
    db: DBDep,
    skip: int = 0,
    limit: int = 100
) -> list[SMessageGet]:
    """
    Получить все сообщения (пагинация).
    Временный endpoint для тестирования.
    """
    return await MessageService(db).get_messages(skip=skip, limit=limit)


@router.get("/user/{user_id}", summary="Получить сообщения пользователя")
async def get_user_messages(
    db: DBDep,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[SMessageGet]:
    """
    Получить сообщения конкретного пользователя
    (входящие и исходящие).
    """
    return await MessageService(db).get_user_messages(
        user_id=user_id,
        skip=skip,
        limit=limit
    )


@router.get("/{message_id}", summary="Получить конкретное сообщение")
async def get_message(
    db: DBDep,
    message_id: int,
) -> SMessageGet:
    """
    Получить сообщение по ID.
    """
    try:
        return await MessageService(db).get_message(message_id=message_id)
    except MessageNotFoundError:
        raise MessageNotFoundHTTPError


@router.delete("/{message_id}", summary="Удалить сообщение")
async def delete_message(
    db: DBDep,
    message_id: int,
    current_user_id: int = 1  # ← Временное решение
) -> dict[str, str]:
    """
    Удалить сообщение (только своё).
    """
    try:
        await MessageService(db).delete_user_message(
            message_id=message_id,
            user_id=current_user_id
        )
        return {"status": "OK", "message": "Сообщение удалено"}
    except MessageNotFoundError:
        raise MessageNotFoundHTTPError
    except MessageAccessDeniedError:
        raise MessageAccessDeniedHTTPError


# ==================== ЗАГЛУШКИ ДЛЯ ЧАТОВ ====================
# (Оставляем для будущего, но возвращаем пустые данные)

@router.get("/conversations", summary="Получение списка всех чатов (заглушка)")
async def get_all_conversations(
    db: DBDep,
    user_id: Optional[int] = None,
) -> list[SConversationList]:
    """
    Заглушка для чатов. Вернётся, когда реализуем систему чатов.
    """
    return []  # ← Пока пустой список


@router.get("/conversations/{conversation_id}", summary="Получение конкретного чата (заглушка)")
async def get_conversation(
    db: DBDep,
    conversation_id: int,
) -> SConversationGet:
    """
    Заглушка для чата. Вернётся, когда реализуем систему чатов.
    """
    # Возвращаем заглушку
    return SConversationGet(
        id=conversation_id,
        partner_name="Заглушка",
        last_message="Чат пока не реализован",
        unread_count=0,
        last_message_time="2024-01-01T00:00:00"
    )