# app/api/reviews.py
from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.reviews import (
    ReviewNotFoundError,
    ReviewNotFoundHTTPError,
    ReviewAlreadyExistsError,
    ReviewAlreadyExistsHTTPError
)
from app.schemes.reviews import (
    SReviewAdd,
    SReviewGet,
    SReviewUpdate,
    SReviewPatch,
    SReviewFilter
)
from app.services.reviews import ReviewService
from app.api.dependencies import DBDep  # <-- Добавьте этот импорт!

router = APIRouter(prefix="/reviews", tags=["Отзывы"])


@router.post("", summary="Создание нового отзыва")
async def create_new_review(
    review_data: SReviewAdd,
    db: DBDep  # <-- Добавьте этот параметр!
) -> dict[str, str]:
    try:
        await ReviewService(db).create_review(review_data)  # <-- Передайте db!
    except ReviewAlreadyExistsError:
        raise ReviewAlreadyExistsHTTPError
    return {"status": "OK"}


@router.get("", summary="Получение списка всех отзывов")
async def get_all_reviews(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    item_id: Optional[int] = None,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> list[SReviewGet]:
    filters = SReviewFilter(item_id=item_id, user_id=user_id)
    return await ReviewService(db).get_reviews(filters=filters, skip=skip, limit=limit)  # <-- Передайте db!


@router.get("/{id}", summary="Получение конкретного отзыва")
async def get_review(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    id: int,
) -> SReviewGet:
    return await ReviewService(db).get_review(review_id=id)  # <-- Передайте db!


@router.put("/{id}", summary="Изменение конкретного отзыва")
async def update_review(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    review_data: SReviewUpdate,
    id: int,
) -> dict[str, str]:
    try:
        await ReviewService(db).edit_review(review_id=id, review_data=review_data)  # <-- Передайте db!
    except ReviewNotFoundError:
        raise ReviewNotFoundHTTPError

    return {"status": "OK"}


@router.patch("/{id}", summary="Частичное изменение конкретного отзыва")
async def patch_review(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    review_data: SReviewPatch,
    id: int,
) -> dict[str, str]:
    try:
        await ReviewService(db).patch_review(review_id=id, review_data=review_data)  # <-- Передайте db!
    except ReviewNotFoundError:
        raise ReviewNotFoundHTTPError

    return {"status": "OK"}


@router.delete("/{id}", summary="Удаление конкретного отзыва")
async def delete_review(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    id: int,
) -> dict[str, str]:
    try:
        await ReviewService(db).delete_review(review_id=id)  # <-- Передайте db!
    except ReviewNotFoundError:
        raise ReviewNotFoundHTTPError

    return {"status": "OK"}


@router.get("/item/{item_id}", summary="Получение отзывов для товара")
async def get_item_reviews(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    item_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[SReviewGet]:
    return await ReviewService(db).get_item_reviews(item_id=item_id, skip=skip, limit=limit)  # <-- Передайте db!


@router.get("/item/{item_id}/average-rating", summary="Получение среднего рейтинга товара")
async def get_item_average_rating(
    db: DBDep,  # <-- Добавьте ПЕРВЫМ параметром!
    item_id: int,
) -> dict[str, float]:
    return {"average_rating": await ReviewService(db).get_item_average_rating(item_id=item_id)}  # <-- Передайте db!