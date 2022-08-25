from project.dao.base import BaseDAO
from project.models import Movie


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

# вариант перенести сюда фильтрацию по статусу
#     def get_all_order_by(self, filter: Optional[str] = None, page: Optional[int] = None) -> List[T]:
#         stmt: BaseQuery = self._db_session.query(self.__model__)
#
#         if filter == 'new':
#             stmt = stmt.order_by(desc(self.__model__.year))
#         else:
#             stmt = stmt.order_by(self.__model__.year)
#
#         if page:
#             try:
#                 return stmt.paginate(page, self._items_per_page).items
#             except NotFound:
#                 return []
#         return stmt.all()
