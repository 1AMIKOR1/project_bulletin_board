# app/repositories/category_repository.py
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.categories import CategoryModel
from app.schemes.categories import SCategoryGet, SCategoryGetWithItems
from .base import BaseRepository


class CategoriesRepository(BaseRepository):
    model = CategoryModel
    schema = SCategoryGet

    async def get_one_or_none_with_items(self, **filter_by):
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(selectinload(self.model.items))
        )

        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if model is None:
            return None

        result = SCategoryGetWithItems.model_validate(model, from_attributes=True)
        return result

    async def get_by_name(self, name: str):
        return await self.get_one_or_none(name=name)
