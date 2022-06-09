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
from reinsurance_db import api_db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():

    _login = request.form.get('login')
    _password = request.form.get('password')

    agent = api_db.db_command(command=f"SELECT idagent, password, name, surname, sec_name, login, qualification "
                                      f"FROM agent WHERE login = '{_login}';")

    if not agent or not check_password_hash(str(agent[1]), str(_password)):
        flash('Ошибка авторизации. Пожалуйста проверьте введенные вами данные и повторите попытку.')
        return redirect(url_for('auth.login'))

    session['loggedin'] = True
    session['idagent'] = agent[0]
    session['name'] = agent[2]
    session['surname'] = agent[3]
    session['sec_name'] = agent[4]
    session['login'] = agent[5]
    session['qualification'] = agent[6]

    if request.form.getlist('not_exist'):
        session.permanent = True
    else:
        session.permanent = False

    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    _login = request.form.get('login')
    _name = request.form.get('name')
    _surname = request.form.get('surname')
    _sec_name = request.form.get('sec_name')
    _qualification = request.form.get('qualification')
    _password = request.form.get('password')
    _hash_password = generate_password_hash(_password)

    pas = api_db.db_command(command=f"SELECT password FROM agent WHERE login = '{_login}';")

    if pas:
        flash('Пользователь с указаным логином уже существует')
        return redirect(url_for('auth.signup'))

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

        #return json.dumps(data)
        return redirect(url_for('auth.login'))

    return redirect(url_for('auth.signup'))


@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    session.pop('surname', None)
    session.pop('sec_name', None)
    session.pop('login', None)
    session.pop('qualification', None)
    return redirect(url_for('auth.login'))

# language = request.args.get('language')
# hash = generate_password_hash("secret password")
# check_password_hash(hash, "secret password")
