from flask_restx import fields, Model

from project.setup.api import api


genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})


director: Model = api.model('Режиссёр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тейлор Шеридан'),
})


user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='smitt@gmail.com'),
    'password': fields.String(required=True, max_length=100, example='Zxc123/*cv'),
    'name': fields.String(required=True, max_length=100, example='Sergey'),
    'surname': fields.String(required=True, max_length=100, example='Sergeev'),
    'favorite_genre': fields.String(required=True, max_length=100, example='Комедия'),
})


movie: Model = api.model('Кинофильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=255, example='Омерзительная восьмерка'),
    'description': fields.String(required=True, max_length=100, example='США после Гражданской войны'),
    'trailer': fields.String(required=True, max_length=100, example='https://www.youtube.com/watch?v=lmB9VWm0okU'),
    'year': fields.String(required=True, example=2015),
    'rating': fields.Float(required=True, example=7.8),
    'genre_id': fields.Integer(required=True, example=1),
    'director_id': fields.Integer(required=True, example=1)
})
