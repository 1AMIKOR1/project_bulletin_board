# app/services/items.py
from typing import Optional
from app.exceptions.items import ItemNotFoundError, ItemAlreadyExistsError
from app.schemes.items import SItemCreate, SItemUpdate, SItemPatch, SItemFilter
from app.services.base import BaseService


class ItemService(BaseService):
    def __init__(self, db):  # <-- Уберите значение по умолчанию None!
        super().__init__(db)

    async def create_item(self, item_data: SItemCreate):
        try:
            # ИСПРАВЬТЕ: create() → add() (как в категориях)
            new_item = await self.db.items.add(item_data)  # <-- Используйте add(), а не create()
            await self.db.commit()
            return new_item
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_item(self, item_id: int):
        item = await self.db.items.get_one_or_none(id=item_id)
        if not item:
            raise ItemNotFoundError
        return item

    async def update_item(self, item_id: int, item_data: SItemUpdate):
        item = await self.db.items.get_one_or_none(id=item_id)
        if not item:
            raise ItemNotFoundError
        # ИСПРАВЬТЕ: update() → edit() (как в категориях)
        await self.db.items.edit(item_data, id=item_id)  # <-- Используйте edit(), а не update()
        await self.db.commit()

        # Получаем обновленный объект
        updated_item = await self.db.items.get_one_or_none(id=item_id)
        return updated_item

    async def patch_item(self, item_id: int, item_data: SItemPatch):
        item = await self.db.items.get_one_or_none(id=item_id)
        if not item:
            raise ItemNotFoundError
        # ИСПРАВЬТЕ: update() → edit() с exclude_unset=True
        await self.db.items.edit(
            item_data,
            id=item_id,
            exclude_unset=True  # <-- Для частичного обновления
        )
        await self.db.commit()
        return

    async def delete_item(self, item_id: int):
        item = await self.db.items.get_one_or_none(id=item_id)
        if not item:
            raise ItemNotFoundError
        # Метод delete() уже делает commit внутри себя!
        await self.db.items.delete(id=item_id)
        # НЕ вызывайте await self.db.commit() здесь!
        return

    async def get_items(self, filters: SItemFilter = None, skip: int = 0, limit: int = 100):
        if filters:
            # Используйте get_filtered для фильтрации
            filter_dict = filters.model_dump(exclude_unset=True)
            return await self.db.items.get_filtered(
                limit=limit,
                offset=skip,
                **filter_dict
            )
        return await self.db.items.get_all()

    async def get_user_items(self, user_id: int, skip: int = 0, limit: int = 100):
        # Используйте get_filtered с фильтром по user_id
        return await self.db.items.get_filtered(
            limit=limit,
            offset=skip,
            user_id=user_id
        )