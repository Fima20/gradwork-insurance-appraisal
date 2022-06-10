import threading
import requests
import argparse
import os
import json
import functools
import utils

from flask import Blueprint, Flask, flash, request, session, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

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


@main.route('/contracts', methods=['GET'])
@check_login
def contracts():
    return redirect(url_for('main.contracts_add'))


@main.route('/contracts/add', methods=['GET'])
@check_login
def contracts_add(num_contracts=DEFAULT_LOAD_IN_PAGE):
    data_contract_list = utils.list_dict_contracts(api_db.get_contracts()[0:num_contracts], num_contracts)
    return render_template('contract_update.html',
                           data_contract_list=data_contract_list,
                           not_button_add=True,
                           contract_status=request.args.get('contract_status'))


@main.route("/contracts/add/<int:id_contract>")
@check_login
def contract_add_get(id_contract,
                     num_contracts=DEFAULT_LOAD_IN_PAGE):
    data_contract = utils.dict_contracts(id_contract)
    data_contract_list = utils.list_dict_contracts(api_db.get_contracts()[0:num_contracts], num_contracts)
    return render_template('contract_update.html',
                           data_contract_list=data_contract_list,
                           data_contract=data_contract,
                           contract_status=request.args.get('contract_status'))


@main.route('/contracts/add', methods=['POST'])
@check_login
def contracts_add_post():

    company_name = request.form.get('company_name')
    id_company = api_db.getid_company(name=company_name)
    if id_company:
        company_create = api_db.update_company(name=company_name, idcompany=id_company)
    else:
        company_create = api_db.add_company(name=company_name)
        id_company = api_db.getid_company(name=company_name)
    if not company_create: return redirect(url_for('main.contracts_add', contract_status="error"))

    passport_series = request.form.get('client_passport_series')
    passport_id = request.form.get('client_passport_id')
    id_client = api_db.getid_client(passport_series=passport_series, passport_id=passport_id)
    print(type(passport_series), type(passport_id), id_client)
    if id_client:
        client_create = api_db.update_client(name=request.form.get('client_name'),
                                             surname=request.form.get('client_surname'),
                                             sec_name=request.form.get('client_sec_name'),
                                             passport_series=passport_series,
                                             passport_id=passport_id,
                                             idclient=id_client)
    else:
        client_create = api_db.add_client(name=request.form.get('client_name'),
                                          surname=request.form.get('client_surname'),
                                          sec_name=request.form.get('client_sec_name'),
                                          passport_series=passport_series,
                                          passport_id=passport_id)
        id_client = api_db.getid_client(passport_series=passport_series, passport_id=passport_id)
    if not client_create: return redirect(url_for('main.contracts_add', contract_status="error"))

    title = request.form.get('type_insurance_name')
    short_title = request.form.get('type_insurance_small_name')
    id_insurance_type = api_db.getid_insurance_type(title=title, short_title=short_title)
    if id_insurance_type:
        insurance_type_create = api_db.update_insurance_type(title=title,
                                                             short_title=request.form.get('type_insurance_small_name'),
                                                             capital=request.form.get('type_insurance_capital'),
                                                             idinsurance_type=id_insurance_type)
    else:
        insurance_type_create = api_db.add_insurance_type(title=title,
                                                          short_title=request.form.get('type_insurance_small_name'),
                                                          capital=request.form.get('type_insurance_capital'))
        id_insurance_type = api_db.getid_insurance_type(title=title)
    if not insurance_type_create: return redirect(url_for('main.contracts_add', contract_status="error"))

    insurance_amount = request.form.get('insurance_amount')
    insurance_payment = request.form.get('insurance_payment')
    date_start = request.form.get('date_start')
    date_stop = request.form.get('date_stop')
    id_unit = api_db.getid_default_unit()
    id_agent = session['idagent']

    id_contract = api_db.getid_contract(id_client=id_client)
    if id_contract:
        contract_create = api_db.update_contract(id_client=id_client,
                                                 id_company=id_company,
                                                 id_unit=id_unit,
                                                 id_insurance_type=id_insurance_type,
                                                 id_agent=id_agent,
                                                 insurance_amount=insurance_amount,
                                                 insurance_payment=insurance_payment,
                                                 date_start=date_start,
                                                 date_stop=date_stop,
                                                 idcontract=id_contract)
        contract_status = "update"
    else:
        contract_create = api_db.add_contract(id_client=id_client,
                                              id_company=id_company,
                                              id_unit=id_unit,
                                              id_insurance_type=id_insurance_type,
                                              id_agent=id_agent,
                                              insurance_amount=insurance_amount,
                                              insurance_payment=insurance_payment,
                                              date_start=date_start,
                                              date_stop=date_stop)
        id_contract = api_db.getid_contract(id_client=id_client)
        contract_status = "create"

    if not contract_create: return redirect(url_for('main.contracts_add', contract_status="error"))
    return redirect(url_for('main.contract_add_get',
                            id_contract=id_contract,
                            contract_status=contract_status))
