from app.database.database import async_session_maker
from app.repositories.users import UsersRepository
from app.repositories.items import ItemsRepository
from app.repositories.categories import CategoriesRepository
from app.repositories.locations import LocationsRepository
from app.repositories.messages import MessagesRepository
from app.repositories.reviews import ReviewsRepository
from app.repositories.roles import RolesRepository


class DBManager:
    def __init__(self, session_factory: async_session_maker):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        # TODO Добавить сюда созданные репозитории
        # Пример:
        self.users = UsersRepository(self.session)
        self.items = ItemsRepository(self.session)
        self.categories = CategoriesRepository(self.session)
        self.locations = LocationsRepository(self.session)
        self.messages = MessagesRepository(self.session)
        self.reviews = ReviewsRepository(self.session)
        self.roles = RolesRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
