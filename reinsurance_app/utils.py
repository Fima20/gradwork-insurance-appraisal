import threading
import requests
import argparse
import os
import json
import functools
import time

from flask import Blueprint, Flask, flash, request, session, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from reinsurance_db import api_db


def debug_time(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter_ns()
        res = function(*args, **kwargs)
        print(str(function.__name__) + " - " + str((time.perf_counter_ns() - start_time)/100000))
        return res
    return wrapper


def debug_numdef(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)

    return wrapper


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


def dict_contracts_old(id_contract):
    contract_db = api_db.get_contract(id_contract=id_contract)

    client_db = api_db.get_client(id_client=contract_db[1])
    client = {'name': client_db[1],
              'surname': client_db[2],
              'sec_name': client_db[3],
              'passport_series': client_db[4],
              'passport_id': client_db[5]}

    company_db = api_db.get_company(id_company=contract_db[2])
    company = {'name': company_db[1]}

    insurance_type_db = api_db.get_insurance_type(id_insurance_type=contract_db[4])
    insurance_type = {'title': insurance_type_db[1],
                      'short_title': insurance_type_db[2],
                      'capital': insurance_type_db[3]}

    agent_db = api_db.get_agent(id_agent=contract_db[5])
    agent = {'name': agent_db[1],
             'surname': agent_db[2],
             'sec_name': agent_db[3]}

    data_contract = {'client': client,
                     'company': company,
                     'insurance_type': insurance_type,
                     'agent': agent,
                     'insurance_amount': contract_db[6],
                     'insurance_payment': contract_db[7],
                     'date_start': contract_db[8],
                     'date_stop': contract_db[9],
                     'idcontract': id_contract}

    return data_contract


def dict_contracts(id_contract):
    contract_db = api_db.get_full_contract(id_contract=id_contract)

    client = {'name': contract_db[11],
              'surname': contract_db[12],
              'sec_name': contract_db[13],
              'passport_series': contract_db[14],
              'passport_id': contract_db[15]}

    company = {'name': contract_db[17]}

    insurance_type = {'title': contract_db[27],
                      'short_title': contract_db[28],
                      'capital': contract_db[29]}

    agent = {'name': contract_db[19],
             'surname': contract_db[20],
             'sec_name': contract_db[21]}

    data_contract = {'client': client,
                     'company': company,
                     'insurance_type': insurance_type,
                     'agent': agent,
                     'insurance_amount': contract_db[6],
                     'insurance_payment': contract_db[7],
                     'date_start': contract_db[8],
                     'date_stop': contract_db[9],
                     'idcontract': id_contract}

    return data_contract


def list_dict_contracts(list_contract, num=10):
    res_list = []
    if num > len(list_contract): num = len(list_contract)
    for iter in range(num):
        res_list.append(dict_contracts(list_contract[iter][0]))
    return res_list
