import json
from flask import request
from flask_restx import Namespace, Resource
from project.container import auth_service

api = Namespace('auth')


@api.route('/register/')
class UserRegister(Resource):
    def post(self):
        req_json = request.json
        user = auth_service.create(req_json)
        return "", 201, {"location": f"/auth/{user.id}"}

@api.route('/login/')
class UserLogin(Resource):
    def post(self):
        req_json = request.json
        user_data = auth_service.check_user(req_json)
        if "email" and "name" not in user_data:
            return user_data
        else:
            tokens = json.dumps(auth_service.generate_tokens(user_data))
            return tokens, 201

    def put(self):
        req_json = request.json
        user_data = auth_service.refresh_token(req_json)
        if "email" and "name" not in user_data:
            return user_data
        else:
            tokens = json.dumps(auth_service.generate_tokens(user_data))
            return tokens, 201