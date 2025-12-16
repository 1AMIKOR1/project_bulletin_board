# app/services/auth.py
from datetime import datetime, timezone, timedelta
from app.config import settings
from app.exceptions.auth import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidPasswordError,
    InvalidJWTTokenError,
    JWTTokenExpiredError,
)
from app.exceptions.base import ObjectAlreadyExistsError
from app.schemes.users import (
    SUserAdd,
    SUserAddRequest,
    SUserAuth,
)
from app.schemes.relations_users_roles import SUserGetWithRels
from app.schemes.auth import STokenResponse, SUserResponse
from app.services.base import BaseService
import jwt
from passlib.context import CryptContext


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire: datetime = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire, "type": "access"}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire: datetime = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode |= {"exp": expire, "type": "refresh"}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, plain_password) -> str:
        return cls.pwd_context.hash(plain_password)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
        except jwt.exceptions.DecodeError as ex:
            raise InvalidJWTTokenError from ex
        except jwt.exceptions.ExpiredSignatureError as ex:
            raise JWTTokenExpiredError from ex

    async def register_user(self, user_data: SUserAddRequest):
        # Проверяем, существует ли пользователь с таким email
        existing_user = await self.db.users.get_one_or_none(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsError

        # Проверяем, существует ли роль
        from app.services.roles import RolesService
        role_service = RolesService(self.db)
        role = await role_service.get_role_by_id(1)
        if not role:
            from app.exceptions.roles import RoleNotFoundError
            raise RoleNotFoundError

        hashed_password: str = self.hash_password(user_data.password)
        new_user_data = SUserAdd(
            email=user_data.email,
            hashed_password=hashed_password,
            name=user_data.name,
            role_id=1
        )
        user = await self.db.users.add(new_user_data)
        await self.db.commit()
        return user

    async def login_user(self, user_data: SUserAuth):
        user = await self.db.users.get_one_or_none(email=user_data.email)
        if not user:
            raise UserNotFoundError

        if not self.verify_password(user_data.password, user.hashed_password):
            raise InvalidPasswordError

        token_data = {"user_id": user.id, "email": user.email}
        access_token = self.create_access_token(token_data)

        return access_token
        # return STokenResponse(
        #     token=access_token,
        #     user=SUserResponse(
        #         id=user.id,
        #         name=user.name,
        #         # name=user.full_name or user.email.split('@')[0],  # Используем email как имя, если full_name пустое
        #         email=user.email,
        #         trust_score=getattr(user, 'trust_score', 5.0)
        #     )
        # )

    async def get_me(self, user_id: int) -> SUserGetWithRels:
        user = await self.db.users.get_one_or_none_with_role(id=user_id)
        if not user:
            raise UserNotFoundError

        return user