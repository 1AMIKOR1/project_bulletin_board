# app/api/items.py
from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.items import (
    ItemNotFoundError,
    ItemNotFoundHTTPError,
    ItemAlreadyExistsError,
    ItemAlreadyExistsHTTPError
)
from app.schemes.items import (
    SItemAdd,
    SItemGet,
    SItemUpdate,
    SItemPatch,
    SItemFilter
)
from app.services.items import ItemService
from app.api.dependencies import DBDep  # <-- Добавьте этот импорт!

router = APIRouter(prefix="/items", tags=["Товары"])


@router.post("", summary="Создание нового товара")
async def create_new_item(
    item_data: SItemAdd,
    db: DBDep  # <-- Добавьте этот параметр!
) -> dict[str, str]:
    try:
        await ItemService(db).create_item(item_data)  # <-- Передайте db!
    except ItemAlreadyExistsError:
        raise ItemAlreadyExistsHTTPError
    return {"status": "OK"}


@router.get("", summary="Получение списка всех товаров")
async def get_all_items(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    category_id: Optional[int] = None,
    location_id: Optional[int] = None,
    user_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> list[SItemGet]:
    filters = SItemFilter(
        category_id=category_id,
        location_id=location_id,
        user_id=user_id,
        is_active=is_active
    )
    return await ItemService(db).get_items(filters=filters, skip=skip, limit=limit)  # <-- Передайте db!


@router.get("/{id}", summary="Получение конкретного товара")
async def get_item(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    id: int,
) -> SItemGet:
    return await ItemService(db).get_item(item_id=id)  # <-- Передайте db!


@router.put("/{id}", summary="Изменение конкретного товара")
async def update_item(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    item_data: SItemUpdate,
    id: int,
) -> dict[str, str]:
    try:
        await ItemService(db).edit_item(item_id=id, item_data=item_data)  # <-- Передайте db!
    except ItemNotFoundError:
        raise ItemNotFoundHTTPError

    return {"status": "OK"}


@router.patch("/{id}", summary="Частичное изменение конкретного товара")
async def patch_item(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    item_data: SItemPatch,
    id: int,
) -> dict[str, str]:
    try:
        await ItemService(db).patch_item(item_id=id, item_data=item_data)  # <-- Передайте db!
    except ItemNotFoundError:
        raise ItemNotFoundHTTPError

    return {"status": "OK"}


@router.delete("/{id}", summary="Удаление конкретного товара")
async def delete_item(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    id: int,
) -> dict[str, str]:
    try:
        await ItemService(db).delete_item(item_id=id)  # <-- Передайте db!
    except ItemNotFoundError:
        raise ItemNotFoundHTTPError

    return {"status": "OK"}


@router.get("/user/{user_id}", summary="Получение товаров пользователя")
async def get_user_items(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[SItemGet]:
    return await ItemService(db).get_user_items(user_id=user_id, skip=skip, limit=limit)  # <-- Передайте db!