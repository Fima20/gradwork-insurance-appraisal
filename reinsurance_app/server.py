import threading
import requests
import argparse
import os
import json

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

import reinsurance_db.api_db
from config import SERVER_HOST, SERVER_PORT, UPLOAD_FOLDER
from reinsurance_db import api_db

from auth import auth as auth_blueprint
from main import main as main_blueprint
from reanalysis import reanalysis as reanalysis_blueprint


def create_app():

    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    CORS(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(reanalysis_blueprint)

    return app


def runserver(app_flask, host=SERVER_HOST, port=SERVER_PORT, debug=False):
    server = threading.Thread(target=app_flask.run(debug=debug, host=host, port=port))
    server.start()


if __name__ == '__main__':
    app = create_app()
    runserver(app, debug=True)
