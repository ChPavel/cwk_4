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
