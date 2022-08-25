import json
from flask import request
from flask_restx import Namespace, Resource
from project.container import auth_service
from project.tools.security import generate_tokens, refresh_tokens


api = Namespace('auth')


@api.route('/register/')
class UserRegisterView(Resource):
    def post(self):
        """
        Create new user.
        """
        req_json = request.json
        user = auth_service.create_user(req_json)
        return "", 201, {"location": f"/auth/register/{user.id}"}

    # Вариант (требует перестройки auth_service.create):
    #     if req_json.get('email') and req_json.get('password'):
    #         return auth_service.create(email=req_json.get('email'), password=req_json.get('password'))
    #     else:
    #         return "Что то не так", 401

@api.route('/register/<int:uid>/')
class UsersView(Resource):
    def delete(self, uid):
        """
        Delete user.
        """
        print(uid)
        auth_service.delete(uid)
        return "", 204


@api.route('/login/')
class UserLoginView(Resource):
    def post(self):
        """
        Login user.
        """
        req_json = request.json
        user_data = auth_service.check_user(req_json)
        if "password" and "email" not in user_data:
            return user_data
        else:
            tokens = json.dumps(generate_tokens(user_data))
            return tokens, 201

    # Вариант (требует перестройки auth_service.check_user):
    #     if req_json.get('email') and req_json.get('password'):
    #         return auth_service.generate_tokens(email=req_json.get('email'), password=req_json.get('password'))
    #     else:
    #         return "Что то не так", 401

    def put(self):
        """
        Update token of user.
        """
        req_json = request.json
        user_data = refresh_tokens(req_json)
        if "password" and "email" not in user_data:
            return user_data
        else:
            tokens = json.dumps(generate_tokens(user_data))
            return tokens, 201

    # Вариант (требует перестройки auth_service.refresh_token):
    #     if req_json.get('access_token') and req_json.get('refresh_token'):
    #         return auth_service.refresh_token(access_token=req_json.get('access_token'),
    #         refresh_token=req_json.get('refresh_token'))
    #     else:
    #         return "Что то не так", 401
