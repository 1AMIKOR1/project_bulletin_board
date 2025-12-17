from fastapi import APIRouter

from app.exceptions.categories import (
    CategoryNotFoundError,
    CategoryNotFoundHTTPError,
    CategoryAlreadyExistsError,
    CategoryAlreadyExistsHTTPError,
)
from app.schemes.categories import (
    SCategoryAdd,
    SCategoryGet,
    SCategoryUpdate,
    SCategoryPatch,
)
from app.services.categories import CategoryService
from app.api.dependencies import DBDep
from app.database.db_manager import DBManager

router = APIRouter(prefix="/categories", tags=["Категории"])


@router.post("", summary="Создание новой категории")
async def create_new_category(category_data: SCategoryAdd, db: DBDep) -> dict[str, str]:
    try:
        service = CategoryService(db)
        await service.create_category(category_data)
    except CategoryAlreadyExistsError:
        raise CategoryAlreadyExistsHTTPError
    return {"status": "OK"}


@router.get("", summary="Получение списка всех категорий")
async def get_all_categories(db: DBDep) -> list[SCategoryGet]:
    service = CategoryService(db)
    return await service.get_categories()


@router.get("/{id}", summary="Получение конкретной категории")
async def get_category(id: int, db: DBDep) -> SCategoryGet:
    service = CategoryService(db)
    return await service.get_category(category_id=id)


@router.put("/{id}", summary="Изменение конкретной категории")
async def update_category(
    category_data: SCategoryUpdate, id: int, db: DBDep
) -> dict[str, str]:
    try:
        service = CategoryService(db)
        await service.update_category(category_id=id, category_data=category_data)
    except CategoryNotFoundError:
        raise CategoryNotFoundHTTPError

    return {"status": "OK"}


@router.patch("/{id}", summary="Частичное изменение конкретной категории")
async def patch_category(
    category_data: SCategoryPatch, id: int, db: DBDep
) -> dict[str, str]:
    try:
        service = CategoryService(db)
        await service.patch_category(category_id=id, category_data=category_data)
    except CategoryNotFoundError:
        raise CategoryNotFoundHTTPError

    return {"status": "OK"}


@router.delete("/{id}", summary="Удаление конкретной категории")
async def delete_category(id: int, db: DBDep) -> dict[str, str]:
    try:
        service = CategoryService(db)
        await service.delete_category(category_id=id)
    except CategoryNotFoundError:
        raise CategoryNotFoundHTTPError

    return {"status": "OK"}
