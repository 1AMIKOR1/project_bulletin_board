# app/api/locations.py
from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.locations import (
    LocationNotFoundError,
    LocationNotFoundHTTPError,
    LocationAlreadyExistsError,
    LocationAlreadyExistsHTTPError
)
from app.schemes.locations import (
    SLocationAdd,
    SLocationGet,
    SLocationUpdate,
    SLocationPatch,
    SLocationFilter
)
from app.services.locations import LocationService
from app.api.dependencies import DBDep  # <-- Добавьте этот импорт!

router = APIRouter(prefix="/locations", tags=["Локации"])


@router.post("", summary="Создание новой локации")
async def create_new_location(
    location_data: SLocationAdd,
    db: DBDep  # <-- Добавьте этот параметр!
) -> dict[str, str]:
    try:
        await LocationService(db).create_location(location_data)  # <-- Передайте db!
    except LocationAlreadyExistsError:
        raise LocationAlreadyExistsHTTPError
    return {"status": "OK"}


@router.get("", summary="Получение списка всех локаций")
async def get_all_locations(
    db: DBDep,
    city: Optional[str] = None,
    region: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[SLocationGet]:
    filters = SLocationFilter(city=city, region=region)
    return await LocationService(db).get_locations(filters=filters, skip=skip, limit=limit)

@router.get("/{id}", summary="Получение конкретной локации")
async def get_location(
    id: int,
    db: DBDep  # <-- Добавьте этот параметр!
) -> SLocationGet:
    return await LocationService(db).get_location(location_id=id)  # <-- Передайте db!


@router.put("/{id}", summary="Изменение конкретной локации")
async def update_location(
    location_data: SLocationUpdate,
    id: int,
    db: DBDep  # <-- Добавьте этот параметр!
) -> dict[str, str]:
    try:
        await LocationService(db).edit_location(location_id=id, location_data=location_data)  # <-- Передайте db!
    except LocationNotFoundError:
        raise LocationNotFoundHTTPError

    return {"status": "OK"}


@router.patch("/{id}", summary="Частичное изменение конкретной локации")
async def patch_location(
    location_data: SLocationPatch,
    id: int,
    db: DBDep  # <-- Добавьте этот параметр!
) -> dict[str, str]:
    try:
        await LocationService(db).patch_location(location_id=id, location_data=location_data)  # <-- Передайте db!
    except LocationNotFoundError:
        raise LocationNotFoundHTTPError

    return {"status": "OK"}


@router.delete("/{id}", summary="Удаление конкретной локации")
async def delete_location(
    id: int,
    db: DBDep  # <-- Добавьте этот параметр!
) -> dict[str, str]:
    try:
        await LocationService(db).delete_location(location_id=id)  # <-- Передайте db!
    except LocationNotFoundError:
        raise LocationNotFoundHTTPError

    return {"status": "OK"}