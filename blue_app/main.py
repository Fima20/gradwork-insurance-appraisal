import threading
import requests
import argparse
import os
import json

from flask import Blueprint, Flask, flash, request, session, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from config import SERVER_HOST, SERVER_PORT, UPLOAD_FOLDER
from db_reinsurance import api_db
from utils import login_check

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():

    if not login_check():
        flash('Необходима авторизация')
        return redirect(url_for('auth.login'))

    return render_template('profile.html', name=session["name"])


@main.route('/shutdown')
def shutdown():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@main.route('/contracts')
def contracts():

    if not login_check():
        flash('Необходима авторизация')
        return redirect(url_for('auth.login'))

    return render_template('contracts.html')

