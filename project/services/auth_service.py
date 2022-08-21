import datetime
import calendar
import hashlib
from typing import Optional
import jwt
from flask_restx import abort
from project.constants import SECRET, ALGO
from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.config import BaseConfig


class AuthService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            BaseConfig.PWD_HASH_SALT,
            BaseConfig.PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def generate_tokens(self, user_data):
        # access_token на 30 минут.
        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        user_data['exp'] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(user_data, SECRET, algorithm=ALGO)

        # refresh_token на 130 дней.
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        user_data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(user_data, SECRET, algorithm=ALGO)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_token(self, token):
        refresh_token = token.get("refresh_token", None)

        if refresh_token is None:
            abort(400)

        try:
            data = jwt.decode(refresh_token, SECRET, algorithms=[ALGO])

        except Exception as e:
            abort(401)

        user_data = {
            "name": data['name'],
            "email": data['email']
        }

        return user_data

    def create(self, user_d: dict):
        user_d["password"] = self.get_hash(user_d["password"])
        return self.dao.create(user_d)

    def check_user(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if None in [email, password]:
            abort(400)

        user: User = self.dao.get_user_by_email(email)

        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        password_hash = self.get_hash(password)

        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401

        user_data = {
            "name": user.name,
            "email": user.email
        }
        return user_data

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:   # int | None
        return self.dao.get_all(page=page)