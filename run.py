# from flask_restx import Resource

from project.config import config
from project.models import Genre, Director, User, Movie
from project.server import create_app, db

app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "User": User,
        "Movie": Movie
    }


# @app.route('/')
# class StartView(Resource):
#     def start_page(self):
#         """
#         Главная страница.
#         """
#         return 'Поиск фильмов'


if __name__ == '__main__':                                  # i am
    app.run(host="localhost", port=10001, debug=True)       # I am
