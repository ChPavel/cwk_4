from flask import request
from flask_restx import Namespace, Resource
from project.container import movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import page_parser


api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    @api.expect(page_parser)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all movies.
        """
        # status: str = request.args.get('status')   # вариант перенести из базового DAO во вью и movie_service.
        # return movie_service.get_all(filter=status, **page_parser.parse_args())

        return movie_service.get_all(**page_parser.parse_args())


@api.route('/<int:movie_id>/')
class GenreView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, movie_id: int):
        """
        Get movie by id.
        """
        return movie_service.get_item(movie_id)