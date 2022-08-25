from typing import Optional, List
from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MoviesService:
    """
    Класс сервиса методов для модели Movie по маршрутам /movies.
    """
    def __init__(self, dao: BaseDAO) -> None:  # Для варианта используем вместо BaseDAO - MoviesDAO.
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Movie with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> List[Movie]:   # int | None
        movies = self.dao.get_all(page=page)
        return movies

    # # Вариант: для фильтрации по статусу вместо get_all ставим:
    # def get_all(self, page: Optional[int] = None, filter: Optional[str] = None, ) -> List[Movie]:  # int | None
    #     return self.dao.get_all_order_by(page=page, filter=filter)

