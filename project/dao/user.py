from project.dao.base import BaseDAO
from project.models import User


class UsersDAO(BaseDAO[User]):
    __model__ = User