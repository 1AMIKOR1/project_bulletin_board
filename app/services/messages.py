# app/services/messages.py
from typing import Optional
from app.exceptions.messages import (
    MessageNotFoundError,
    ConversationNotFoundError,
    MessageAccessDeniedError
)
from app.schemes.messages import (
    SMessageCreate,
    SMessageUpdate,
    SMessagePatch,
    SConversationGet,
    SConversationList
)
from app.services.base import BaseService


class MessageService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    # ============ ОСНОВНЫЕ МЕТОДЫ ДЛЯ ПРЯМЫХ СООБЩЕНИЙ ============

    async def send_direct_message(self, message_data: SMessageCreate, current_user_id: int):
        """
        Отправить прямое сообщение другому пользователю.

        Args:
            message_data: Данные сообщения (text, recipient_id, item_id)
            current_user_id: ID текущего пользователя (отправитель)
        """
        try:
            # 1. Подготавливаем данные для модели
            message_dict = message_data.model_dump()

            # 2. Добавляем sender_id (текущий пользователь)
            message_dict["sender_id"] = current_user_id

            # 3. Проверяем и переименовываем поля
            # В схеме: recipient_id, в модели: recipient_id (теперь совпадает!)
            # В схеме: item_id, в модели: item_id (совпадает!)

            # 4. Создаём объект схемы с исправленными данными
            fixed_data = SMessageCreate(**message_dict)

            # 5. Используем add() с ignore_duplicates=True
            new_message = await self.db.messages.add(fixed_data, ignore_duplicates=True)

            if new_message:
                await self.db.commit()
                print(f"✅ Сообщение отправлено. ID: {new_message.id}")
                return new_message
            else:
                # Если add() вернул None (дубликат проигнорирован)
                print("⚠️ Сообщение уже существует или ошибка")
                return {"message": "Сообщение уже существует"}

        except Exception as e:
            await self.db.rollback()
            print(f"❌ Ошибка при отправке сообщения: {e}")
            raise e

    async def get_message(self, message_id: int):
        """Получить сообщение по ID"""
        message = await self.db.messages.get_one_or_none(id=message_id)
        if not message:
            raise MessageNotFoundError
        return message

    async def get_messages(self, skip: int = 0, limit: int = 100):
        """Получить все сообщения (с пагинацией)"""
        return await self.db.messages.get_filtered(
            limit=limit,
            offset=skip
        )

    async def get_user_messages(self, user_id: int, skip: int = 0, limit: int = 100):
        """
        Получить сообщения пользователя (входящие и исходящие).
        Использует специальный метод из репозитория.
        """
        # Проверяем, есть ли метод get_user_messages в репозитории
        if hasattr(self.db.messages, 'get_user_messages'):
            return await self.db.messages.get_user_messages(user_id=user_id)

        # Если нет - используем фильтрацию
        sent = await self.db.messages.get_filtered(
            limit=limit,
            offset=skip,
            sender_id=user_id
        )

        received = await self.db.messages.get_filtered(
            limit=limit,
            offset=skip,
            recipient_id=user_id
        )

        # Объединяем и сортируем по дате
        all_messages = sent + received
        all_messages.sort(key=lambda x: x.created_at, reverse=True)

        return all_messages[:limit]

    async def delete_user_message(self, message_id: int, user_id: int):
        """
        Удалить сообщение (только если пользователь - отправитель)
        """
        message = await self.db.messages.get_one_or_none(id=message_id)

        if not message:
            raise MessageNotFoundError

        # Проверяем права (только отправитель может удалить)
        if message.sender_id != user_id:
            raise MessageAccessDeniedError

        # Удаляем сообщение
        await self.db.messages.delete(id=message_id)
        print(f"✅ Сообщение {message_id} удалено пользователем {user_id}")
        return True

    # ============ БАЗОВЫЕ CRUD МЕТОДЫ ============

    async def create_message(self, message_data: SMessageCreate):
        """Создать сообщение (устаревший метод, используйте send_direct_message)"""
        try:
            new_message = await self.db.messages.add(message_data, ignore_duplicates=True)
            await self.db.commit()
            return new_message
        except Exception as e:
            await self.db.rollback()
            raise e

    async def update_message(self, message_id: int, message_data: SMessageUpdate):
        """Обновить сообщение"""
        message = await self.db.messages.get_one_or_none(id=message_id)
        if not message:
            raise MessageNotFoundError

        await self.db.messages.edit(message_data, id=message_id)
        await self.db.commit()

        updated_message = await self.db.messages.get_one_or_none(id=message_id)
        return updated_message

    async def patch_message(self, message_id: int, message_data: SMessagePatch):
        """Частично обновить сообщение"""
        message = await self.db.messages.get_one_or_none(id=message_id)
        if not message:
            raise MessageNotFoundError

        await self.db.messages.edit(
            message_data,
            id=message_id,
            exclude_unset=True
        )
        await self.db.commit()
        return

    async def delete_message(self, message_id: int):
        """Удалить сообщение (без проверки прав)"""
        message = await self.db.messages.get_one_or_none(id=message_id)
        if not message:
            raise MessageNotFoundError

        await self.db.messages.delete(id=message_id)
        return

    # ============ ЗАГЛУШКИ ДЛЯ ЧАТОВ ============

    async def get_conversations(self, user_id: Optional[int] = None) -> list[SConversationList]:
        """Заглушка для получения чатов"""
        print("⚠️ Метод get_conversations пока не реализован")
        return []

    async def get_conversation(self, conversation_id: int) -> SConversationGet:
        """Заглушка для получения чата"""
        print(f"⚠️ Метод get_conversation пока не реализован (ID: {conversation_id})")
        raise ConversationNotFoundError