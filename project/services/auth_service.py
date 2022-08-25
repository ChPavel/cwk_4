from typing import Optional, List
from flask_restx import abort
from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_password_hash


class AuthService:
    """
    Класс сервиса методов для модели User по маршрутам /auth.
    """
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> List[User]:   # int | None
        return self.dao.get_all(page=page)

    def create_user(self, user_d: dict):
        try:
            user_d["password"] = generate_password_hash(user_d["password"])
            return self.dao.create(user_d)
        except Exception as e:
            return f"Возникла ошибка: {e}"

    def delete(self, uid):
        self.dao.delete(uid)

    def check_user(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if None in [email, password]:
            abort(400)

        user: User = self.dao.get_user_by_email(email)

        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        password_hash = generate_password_hash(password)

        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401

        user_data = {
            "password": user.password,
            "email": user.email
        }
        return user_data

    # # Варианты для auth/register и login:
    # def check_user(self, email, password):
    #     user = self.get_user_by_email(email)
    #     return generate_tokens(email=email, password=password, password_hash=password_hash)
