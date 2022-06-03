import threading
import requests
import argparse
import os
import json

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from utils import config_parser, allowed_file
from config import SERVER_HOST, SERVER_PORT, UPLOAD_FOLDER
from db_reinsurance import api_db


def check_content_type(func):
    def wrap(*args, **kwargs):
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            func(*args, **kwargs)
        else:
            return 'Content-Type not supported!'

    return wrap


class Server:

    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        CORS(self.app)

        self.app.add_url_rule('/', view_func=self.shutdown, methods=['GET'])
        self.app.add_url_rule('/shutdown', view_func=self.shutdown, methods=['GET'])
        self.app.add_url_rule('/api/users/signup', view_func=self.register, methods=['POST'])
        self.app.add_url_rule('/api/users/login', view_func=self.authentication, methods=['POST'])

    def runserver(self):
        self.server = threading.Thread(target=self.app.run(debug=self.debug),
                                       kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server

    def shutdown(self):
        terminate_func = request.environ.get('werkzeug.server.shutdown')
        if terminate_func:
            terminate_func()

    def signup(self):

        req_json = request.get_json()
        _data = req_json.get("data")

        _name = _data.get("name")
        _surname = _data.get("surname")
        _sec_name = _data.get("sec_name")
        _login = _data.get("login")
        _hash_password = generate_password_hash(_data.get("password"))
        _qualification = _data.get("qualification")

        comp = api_db.add_agent(name=_name,
                                surname=_surname,
                                sec_name=_sec_name,
                                login=_login,
                                hash_password=_hash_password,
                                qualification=_qualification)

        if comp:
            data = {
                "data": {
                    "name": _name,
                    "surname": _surname,
                    "sec_name": _sec_name,
                    "login": _login,
                    "qualification": _qualification
                }
            }

            return json.dumps(data)

    def login(self):

        req_json = request.get_json()
        _data = req_json.get("data")

        _login = _data.get("login")
        _hash_password = generate_password_hash(_data.get("password"))
        _qualification = _data.get("qualification")

        comp = api_db.db_command(command="")

        if comp:
            data = {
                "data": {
                    "name": _name,
                    "surname": _surname,
                    "sec_name": _sec_name,
                    "login": _login,
                    "qualification": _qualification
                }
            }

            return json.dumps(data)


    # language = request.args.get('language')
    # hash = generate_password_hash("secret password")
    # check_password_hash(hash, "secret password")


if __name__ == '__main__':
    server = Server(
        host=SERVER_HOST,
        port=SERVER_PORT
    )
    server.runserver()
