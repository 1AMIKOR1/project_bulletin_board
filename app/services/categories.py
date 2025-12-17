# app/services/categories.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from typing import Optional
from app.exceptions.categories import CategoryNotFoundError, CategoryAlreadyExistsError
from app.schemes.categories import SCategoryCreate, SCategoryUpdate, SCategoryPatch
from app.services.base import BaseService


class CategoryService(BaseService):
    def __init__(self, db=None):
        super().__init__(db)

    async def create_category(self, category_data: SCategoryCreate):
        try:
            # Проверка на существование категории по имени
            existing_category = await self.db.categories.get_by_name(category_data.name)
            if existing_category:
                raise CategoryAlreadyExistsError

            # ИСПРАВЛЕНО: create() → add()
            new_category = await self.db.categories.add(category_data)
            await self.db.commit()
            return new_category

        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_category(self, category_id: int):
        category = await self.db.categories.get_one_or_none(id=category_id)
        if not category:
            raise CategoryNotFoundError
        return category

    async def update_category(self, category_id: int, category_data: SCategoryUpdate):
        category = await self.db.categories.get_one_or_none(id=category_id)
        if not category:
            raise CategoryNotFoundError

        # ИСПРАВЛЕНО: update() → edit()
        await self.db.categories.edit(category_data, id=category_id)
        await self.db.commit()

        # Получаем обновленную категорию
        updated_category = await self.db.categories.get_one_or_none(id=category_id)
        return updated_category

    async def patch_category(self, category_id: int, category_data: SCategoryPatch):
        category = await self.db.categories.get_one_or_none(id=category_id)
        if not category:
            raise CategoryNotFoundError

        # ИСПРАВЛЕНО: update() → edit() с exclude_unset=True
        await self.db.categories.edit(
            category_data,
            id=category_id,
            exclude_unset=True
        )
        await self.db.commit()
        return

    async def delete_category(self, category_id: int):
        category = await self.db.categories.get_one_or_none(id=category_id)
        if not category:
            raise CategoryNotFoundError

        # Метод delete() уже есть и он САМ делает commit!
        # Не нужно вызывать await self.db.commit() после него
        await self.db.categories.delete(id=category_id)
        return

    async def get_categories(self):
        return await self.db.categories.get_all()