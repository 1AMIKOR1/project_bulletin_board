from app.models.users import UserModel
from app.repositories.base import BaseRepository
from app.schemes.users import SUserGet


class UsersRepository(BaseRepository):
    model = UserModel
    schema = SUserGet
