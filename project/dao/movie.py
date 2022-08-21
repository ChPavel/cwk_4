from project.dao.base import BaseDAO
from project.models import Movie


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie



