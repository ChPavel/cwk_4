from .director import api as director_ns
from .genres import api as genres_ns
from .movie import api as movie_ns
from project.views.auth.user import api as user_ns


__all__ = [
    'director_ns',
    'genres_ns',
    'movie_ns',
    'user_ns'
]
