from flask_restx import Api, Resource, fields
import jwt
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory

rest_api = Api(version="1.0", title="Users API")

signup_model = rest_api.model(
    'SignUpModel', {
        "username": fields.String(required=True, min_length=2, max_length=32),
        "email": fields.String(required=True, min_length=4, max_length=64),
        "password": fields.String(required=True, min_length=4, max_length=16)
    }
)


@rest_api.route('/api/users/register')
class Register(Resource):
    """
       Регистрация нового пользователя в базе данных с использованием подели `signup_model`.
    """

    @rest_api.expect(signup_model, validate=True)
    def post(self):
        req_data = request.get_json()

        _username = req_data.get("username")
        _email = req_data.get("email")
        _password = req_data.get("password")

        return {
                   "success": True,
                   "user": _username,
                   "msg": "Пользователь успешно зарегистрирован"
               }, 200