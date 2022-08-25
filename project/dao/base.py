from typing import Generic, List, Optional, TypeVar
from sqlalchemy import desc
from flask import current_app, request
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from project.setup.db.models import Base
from project.models import User

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    """
    Базовый класс DAO с универсальными методами и методами для модели User.
    """
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, page: Optional[int] = None) -> List[T]:
        status: str = request.args.get('status')
        part_dbq = self._db_session.query(self.__model__)
        if status == 'new':
            try:
                stmt: BaseQuery = part_dbq.order_by(desc(self.__model__.year))
            except AttributeError:
                stmt: BaseQuery = part_dbq
        elif status == 'old':
            try:
                stmt: BaseQuery = part_dbq.order_by(self.__model__.year)
            except AttributeError:
                stmt: BaseQuery = part_dbq
        else:
            stmt: BaseQuery = part_dbq
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def create(self, user_d: dict):
        user = User(**user_d)
        try:
            self._db_session.add(user)
            self._db_session.commit()
            return user
        except Exception as e:
            self._db_session.rollback()
            print(f"При создании пользователя возникла ошибка: {e}")

    def update_user(self, data, email):
        try:
            self._db_session.query(User).filter(User.email == email).update(data)
            self._db_session.commit()
            print("Пользователь обновлён")
        except Exception as e:
            self._db_session.rollback()
            print(f"При обновлении пользователя возникла ошибка: {e}")

    def get_user_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()

    def delete(self, uid):
        print(uid)
        user = self.get_by_id(uid)
        print(user)
        self._db_session.delete(user)
        self._db_session.commit()