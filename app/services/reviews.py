# app/services/reviews.py
from typing import Optional
from app.exceptions.reviews import ReviewNotFoundError, ReviewAlreadyExistsError
from app.schemes.reviews import SReviewCreate, SReviewUpdate, SReviewPatch, SReviewFilter
from app.services.base import BaseService


class ReviewService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    async def create_review(self, review_data: SReviewCreate):
        """
        Создать новый отзыв
        При обнаружении дубликата возвращает существующий отзыв
        """
        try:
            # Используем add() с ignore_duplicates=True
            # Если отзыв уже существует - вернет существующий объект
            # Если нет - создаст новый
            new_review = await self.db.reviews.add(review_data, ignore_duplicates=True)

            if new_review:
                # Проверяем ID объекта
                if hasattr(new_review, 'id') and new_review.id:
                    # Объект успешно создан или найден - коммитим изменения
                    await self.db.commit()
                    print(f"✅ Отзыв успешно обработан. ID: {new_review.id}")
                    return new_review
                else:
                    # Если объект без ID (маловероятно)
                    print("⚠️ Создан объект без ID")
                    await self.db.commit()
                    return new_review
            else:
                # Если add() вернул None (не смог найти существующий и не создал новый)
                print("⚠️ Не удалось создать или найти отзыв")
                return {"message": "Не удалось создать отзыв"}

        except Exception as e:
            await self.db.rollback()
            print(f"❌ Ошибка при создании отзыва: {e}")
            raise e

    async def get_review(self, review_id: int):
        review = await self.db.reviews.get_one_or_none(id=review_id)
        if not review:
            raise ReviewNotFoundError
        return review

    async def update_review(self, review_id: int, review_data: SReviewUpdate):
        review = await self.db.reviews.get_one_or_none(id=review_id)
        if not review:
            raise ReviewNotFoundError

        # Обновляем отзыв
        await self.db.reviews.edit(review_data, id=review_id)
        await self.db.commit()

        # Получаем обновленный объект
        updated_review = await self.db.reviews.get_one_or_none(id=review_id)
        return updated_review

    async def patch_review(self, review_id: int, review_data: SReviewPatch):
        review = await self.db.reviews.get_one_or_none(id=review_id)
        if not review:
            raise ReviewNotFoundError

        # Частичное обновление
        await self.db.reviews.edit(
            review_data,
            id=review_id,
            exclude_unset=True
        )
        await self.db.commit()
        return

    async def delete_review(self, review_id: int):
        review = await self.db.reviews.get_one_or_none(id=review_id)
        if not review:
            raise ReviewNotFoundError

        # Метод delete() уже делает commit внутри себя!
        await self.db.reviews.delete(id=review_id)
        return

    async def get_reviews(self, filters: SReviewFilter = None, skip: int = 0, limit: int = 100):
        if filters:
            # Используем get_filtered для фильтрации
            filter_dict = filters.model_dump(exclude_unset=True)
            return await self.db.reviews.get_filtered(
                limit=limit,
                offset=skip,
                **filter_dict
            )
        return await self.db.reviews.get_all()

    async def get_item_reviews(self, item_id: int, skip: int = 0, limit: int = 100):
        # Получаем отзывы для конкретного товара
        return await self.db.reviews.get_filtered(
            limit=limit,
            offset=skip,
            item_id=item_id
        )

    async def get_item_average_rating(self, item_id: int):
        # Расчет среднего рейтинга для товара
        reviews = await self.get_item_reviews(item_id=item_id)
        if not reviews:
            return 0.0

        total = sum(review.rating for review in reviews)
        return total / len(reviews)