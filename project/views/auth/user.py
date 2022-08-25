from flask import request
from flask_restx import Namespace, Resource
from project.container import check_token, user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @check_token
    @api.marshal_with(user, code=201, description='OK')
    def get(self):
        """
        Get user.
        """
        token = request.headers['Authorization'].split('Bearer ')[-1]
        return user_service.get_user_by_token(token)

    @check_token
    @api.marshal_with(user, code=201, description='OK')
    def patch(self):
        """
        Patch user.
        """
        token = request.headers['Authorization'].split('Bearer ')[-1]
        data = request.json

        return user_service.update_user(data, token)


@api.route('/password/')
class UpdatePasswordView(Resource):
    @check_token
    @api.marshal_with(user, code=201, description='OK')
    def put(self):
        """
        Update password user.
        """
        data = request.json
        token = request.headers['Authorization'].split('Bearer ')[-1]
        print(f"Дата {data} и Токен {token}")
        if data.get('password_1') and data.get('password_2'):

            return user_service.update_password(data=data, token=token)







