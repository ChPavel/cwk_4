from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'
    __tableargs__ = {'comments': 'Таблица жанров'}

    name = Column(String(100), unique=True, nullable=False, comment="Название")
    movies = relationship("Movie")

    def __repr__(self):
        return f'{self.__tableargs__["comments"]}: ' \
               f'{self.id}, {self.name}'

class Director(models.Base):
    __tablename__ = 'directors'
    __tableargs__ = {'comments': 'Таблица режиссёров'}

    name = Column(String(100), unique=True, nullable=False, comment="Имя")
    movies = relationship("Movie")

    def __repr__(self):
        return f'{self.__tableargs__["comments"]}: ' \
               f'{self.id}, {self.name}'


class User(models.Base):
    __tablename__ = 'users'
    __tableargs__ = {'comments': 'Таблица пользователей'}

    email = Column(String(100), nullable=False, comment="электронная почта")
    password = Column(String(100), nullable=False, comment="пароль")
    name = Column(String(100), comment="Имя")
    surname = Column(String(100), comment="Фамилия")
    favorite_genre = Column(String(100), comment="Любимый жанр")

    def __repr__(self):
        return f'{self.__tableargs__["comments"]}: ' \
               f'{self.id}, {self.name}, {self.surname},' \
               f'{self.email}, ' \
               f'{self.password}, ' \
               f'{self.favorite_genre}'


class Movie(models.Base):
    __tablename__ = 'movies'
    __tableargs__ = {'comments': 'Таблица кинофильмов'}

    title = Column(String(255), nullable=False, comment="Название")
    description = Column(String(255), nullable=False, comment="Описание")
    trailer = Column(String(255), nullable=False, comment="Промо-ролик")
    year = Column(Integer, nullable=False, comment="Год создания")
    rating = Column(Float, nullable=False, comment="Рейтинг")
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)
    director = relationship("Director")

    def __repr__(self):
        return f'{self.__tableargs__["comments"]}: ' \
               f'{self.id}, {self.rating}, {self.year},' \
               f'{self.title}, {self.trailer}' \
               f'{self.director_id}, ' \
               f'{self.genre_id}, {self.director_id}'