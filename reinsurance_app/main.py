import threading
import requests
import argparse
import os
import json
import functools
import utils
import ast

from flask import Blueprint, Flask, flash, request, session, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_modals import Modal

from config import SERVER_HOST, SERVER_PORT, UPLOAD_FOLDER
from reinsurance_db import api_db
from utils import check_login

DEFAULT_LOAD_IN_PAGE = 12

main = Blueprint('main', __name__)


@main.route('/')
@check_login
def index():
    return render_template('index.html')


@main.route('/profile')
@check_login
def profile():
    return render_template('profile.html')


@main.route('/shutdown')
def shutdown():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@main.route('/contracts')
@check_login
def contracts():
    data_contract_list = utils.list_dict_contracts_db(api_db.get_contracts()[0:DEFAULT_LOAD_IN_PAGE], DEFAULT_LOAD_IN_PAGE)
    return render_template('contracts.html',
                           data_contract_list=data_contract_list,
                           contract_status=request.args.get('contract_status'))


@main.route('/contracts/add')
@check_login
def contracts_add():
    data_contract_list = utils.list_dict_contracts_db(api_db.get_contracts()[0:DEFAULT_LOAD_IN_PAGE], DEFAULT_LOAD_IN_PAGE)
    return render_template('contracts_edit.html',
                           data_contract_list=data_contract_list,
                           data_contract=ast.literal_eval(request.args.get('data_contract', default="{}")),
                           not_button_add=True,
                           contract_status=request.args.get('contract_status'))


@main.route("/contracts/edit/<int:id_contract>")
@check_login
def contracts_edit_id(id_contract):
    data_contract = utils.dict_contracts_db(id_contract)
    data_contract_list = utils.list_dict_contracts_db(api_db.get_contracts()[0:DEFAULT_LOAD_IN_PAGE], DEFAULT_LOAD_IN_PAGE)
    return render_template('contracts_edit.html',
                           data_contract_list=data_contract_list,
                           data_contract=data_contract,
                           contract_status=request.args.get('contract_status'))


@main.route('/contracts/add', methods=['POST'])
@check_login
def contracts_add_post():
    id_agent = session['idagent']
    id_unit = api_db.getid_default_unit()
    company_name = request.form.get('company_name')
    passport_series = request.form.get('client_passport_series')
    passport_id = request.form.get('client_passport_id')
    client_name = request.form.get('client_name')
    client_surname = request.form.get('client_surname')
    client_sec_name = request.form.get('client_sec_name')
    insurance_type_title = request.form.get('type_insurance_name')
    insurance_type_short_title = request.form.get('type_insurance_small_name')
    insurance_type_capital = request.form.get('type_insurance_capital')
    contract_insurance_amount = request.form.get('insurance_amount')
    contract_insurance_payment = request.form.get('insurance_payment')
    contract_date_start = request.form.get('date_start')
    contract_date_stop = request.form.get('date_stop')

    status, id_contract_db = api_db.complex_update_contract(id_agent=id_agent,
                                                            id_unit=id_unit,
                                                            company_name=company_name,
                                                            passport_series=passport_series,
                                                            passport_id=passport_id,
                                                            client_name=client_name,
                                                            client_surname=client_surname,
                                                            client_sec_name=client_sec_name,
                                                            insurance_type_title=insurance_type_title,
                                                            insurance_type_short_title=insurance_type_short_title,
                                                            insurance_type_capital=insurance_type_capital,
                                                            contract_insurance_amount=contract_insurance_amount,
                                                            contract_insurance_payment=contract_insurance_payment,
                                                            contract_date_start=contract_date_start,
                                                            contract_date_stop=contract_date_stop)

    print(id_contract_db)
    if status == "error":
        data_contract = utils.dict_contracts_value(id_agent=id_agent,
                                                   company_name=company_name,
                                                   passport_series=passport_series,
                                                   passport_id=passport_id,
                                                   client_name=client_name,
                                                   client_surname=client_surname,
                                                   client_sec_name=client_sec_name,
                                                   insurance_type_title=insurance_type_title,
                                                   insurance_type_short_title=insurance_type_short_title,
                                                   insurance_type_capital=insurance_type_capital,
                                                   contract_insurance_amount=contract_insurance_amount,
                                                   contract_insurance_payment=contract_insurance_payment,
                                                   contract_date_start=contract_date_start,
                                                   contract_date_stop=contract_date_stop)
        return redirect(url_for('main.contracts_add',
                                data_contract=data_contract,
                                contract_status=status))
    else:
        return redirect(url_for('main.contracts_edit_id',
                                id_contract=id_contract_db,
                                contract_status=status))


@main.route('/contracts/edit/<int:id_contract>', methods=['POST'])
@check_login
def contracts_edit_id_post(id_contract=None):
    status, id_contract_db = api_db.complex_update_contract(id_agent=session['idagent'],
                                                            id_unit=api_db.getid_default_unit(),
                                                            company_name=request.form.get('company_name'),
                                                            passport_series=request.form.get('client_passport_series'),
                                                            passport_id=request.form.get('client_passport_id'),
                                                            client_name=request.form.get('client_name'),
                                                            client_surname=request.form.get('client_surname'),
                                                            client_sec_name=request.form.get('client_sec_name'),
                                                            insurance_type_title=request.form.get(
                                                                'type_insurance_name'),
                                                            insurance_type_short_title=request.form.get(
                                                                'type_insurance_small_name'),
                                                            insurance_type_capital=request.form.get(
                                                                'type_insurance_capital'),
                                                            contract_insurance_amount=request.form.get(
                                                                'insurance_amount'),
                                                            contract_insurance_payment=request.form.get(
                                                                'insurance_payment'),
                                                            contract_date_start=request.form.get('date_start'),
                                                            contract_date_stop=request.form.get('date_stop'))

    if status == "error":
        if id_contract:
            return redirect(url_for('main.contracts_edit_id',
                                    id_contract=id_contract,
                                    contract_status="error"))
        else:
            return redirect(url_for('main.contracts_add', contract_status="error"))

    return redirect(url_for('main.contracts_edit_id',
                            id_contract=id_contract_db,
                            contract_status=status))
