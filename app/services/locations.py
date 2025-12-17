# app/services/locations.py
from typing import Optional
from app.exceptions.locations import LocationNotFoundError, LocationAlreadyExistsError
from app.schemes.locations import SLocationCreate, SLocationUpdate, SLocationPatch, SLocationFilter
from app.services.base import BaseService


class LocationService(BaseService):
    def __init__(self, db):  # <-- Уберите значение по умолчанию None!
        super().__init__(db)

    async def create_location(self, location_data: SLocationCreate):
        try:
            # ИСПРАВЬТЕ: create() → add() (как в категориях)
            new_location = await self.db.locations.add(location_data)  # <-- Используйте add(), а не create()
            await self.db.commit()
            return new_location
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_location(self, location_id: int):
        location = await self.db.locations.get_one_or_none(id=location_id)
        if not location:
            raise LocationNotFoundError
        return location

    async def update_location(self, location_id: int, location_data: SLocationUpdate):
        location = await self.db.locations.get_one_or_none(id=location_id)
        if not location:
            raise LocationNotFoundError
        # ИСПРАВЬТЕ: update() → edit() (как в категориях)
        await self.db.locations.edit(location_data, id=location_id)  # <-- Используйте edit(), а не update()
        await self.db.commit()

        # Получаем обновленный объект
        updated_location = await self.db.locations.get_one_or_none(id=location_id)
        return updated_location

    async def patch_location(self, location_id: int, location_data: SLocationPatch):
        location = await self.db.locations.get_one_or_none(id=location_id)
        if not location:
            raise LocationNotFoundError
        # ИСПРАВЬТЕ: update() → edit() с exclude_unset=True
        await self.db.locations.edit(
            location_data,
            id=location_id,
            exclude_unset=True  # <-- Для частичного обновления
        )
        await self.db.commit()
        return

    async def delete_location(self, location_id: int):
        location = await self.db.locations.get_one_or_none(id=location_id)
        if not location:
            raise LocationNotFoundError
        # Метод delete() уже делает commit внутри себя!
        await self.db.locations.delete(id=location_id)
        # НЕ вызывайте await self.db.commit() здесь!
        return

    async def get_locations(self, filters: SLocationFilter = None, skip: int = 0, limit: int = 100):
        if filters:
            # Используйте get_filtered для фильтрации
            filter_dict = filters.model_dump(exclude_unset=True)
            return await self.db.locations.get_filtered(
                limit=limit,
                offset=skip,
                **filter_dict
            )
        return await self.db.locations.get_all()