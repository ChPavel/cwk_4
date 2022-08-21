from project.dao.base import BaseDAO
from project.models import User


class AuthDAO(BaseDAO[User]):
    __model__ = User