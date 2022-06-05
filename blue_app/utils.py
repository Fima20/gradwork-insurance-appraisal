import threading
import requests
import argparse
import os
import json
import functools

from flask import Blueprint, Flask, flash, request, session, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from config import SERVER_HOST, SERVER_PORT, UPLOAD_FOLDER
from db_reinsurance import api_db


def check_loggedin():
    if 'loggedin' in session:
        return True
    return False


def check_login(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not check_loggedin():
            flash('Необходима авторизация')
            return redirect(url_for('auth.login'))
        else:
            return func(*args, **kwargs)

    return wrapper
