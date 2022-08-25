from typing import Optional, List
from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import get_data_by_token, generate_password_hash


class UsersService:
    """
    Класс сервиса методов для модели User по маршрутам /user.
    """
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> List[User]:   # int | None
        return self.dao.get_all(page=page)

    def get_user_by_email(self, email):
        return self.dao.get_user_by_email(email=email)

    def get_user_by_token(self, token):
        data = get_data_by_token(token)
        if data:
            user = self.dao.get_user_by_email(data.get("email"))
            user.password = "*****"
            return user
        else:
            print(f"Ошибка в получении пользователя по токену.")

    def update_user(self, data, token):
        user = get_data_by_token(token)
        data["password"] = generate_password_hash(data["password"])
        if user:
            self.dao.update_user(data=data, email=user.get("email"))

            return self.get_user_by_email(data.get("email"))

    def update_password(self, data, token):
        user = get_data_by_token(token)
        print(f"Юзер: {user}")
        if user:
            self.dao.update_user(
                data={
                    "password": generate_password_hash(data.get("password_2"))
                },
                email=user.get("email"))
            print(f"Дата: {data}")
            print(f"почта: {user.get('email')}")
            return self.dao.get_user_by_email(user.get("email"))
        else:
            print(f"Ошибка в обновлении пароля.")
