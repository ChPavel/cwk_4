from project.dao.base import BaseDAO
from project.models import Director


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director