import jwt
from flask import request, abort
from project.tools.security import get_data_by_token

from project.dao import GenresDAO
from project.dao import DirectorsDAO
from project.dao import MoviesDAO
from project.dao import UsersDAO
from project.dao import AuthDAO

from project.services import GenresService
from project.services import DirectorsService
from project.services import MoviesService
from project.services import UsersService
from project.services import AuthService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorsDAO(db.session)
movie_dao = MoviesDAO(db.session)
user_dao = UsersDAO(db.session)
auth_dao = AuthDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UsersService(dao=user_dao)
auth_service = AuthService(dao=auth_dao)


def check_token(func):
    def wrepper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            get_data_by_token(token)
        except Exception as e:
            print(f'Декодирование прошло с ошибкой: {e}')
            abort(401)
        return func(*args, **kwargs)
    return wrepper