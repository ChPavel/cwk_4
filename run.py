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
