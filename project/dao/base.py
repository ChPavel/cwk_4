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
        if status == 'new':
            try:
                stmt: BaseQuery = self._db_session.query(self.__model__).order_by(desc(self.__model__.year))
            except AttributeError:
                stmt: BaseQuery = self._db_session.query(self.__model__)
        else:
            stmt: BaseQuery = self._db_session.query(self.__model__)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def create(self, user_d: dict):
        user = User(**user_d)
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def get_user_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()