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


def login_check():
    if 'loggedin' in session:
        return True
    return False


# def login_check(func):
#     def wrap(*args, **kwargs):
#         if 'loggedin' in session:
#             return func(*args, **kwargs)
#         flash('Please login.')
#         return redirect(url_for('auth.login'))
#     return wrap
