import threading
import requests
import argparse
import os
import json
import functools
import time
import datetime

from flask import Blueprint, Flask, flash, request, session, redirect, url_for, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

from reinsurance_db import api_db


def debug_time(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter_ns()
        res = function(*args, **kwargs)
        print(str(function.__name__) + " - " + str((time.perf_counter_ns() - start_time) / 100000))
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


def dict_contracts_db_old(id_contract):
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


def dict_contracts_db(id_contract):
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


def list_dict_contracts_db(list_contract, num=10):
    res_list = []
    if num > len(list_contract): num = len(list_contract)
    for iter in range(num):
        res_list.append(dict_contracts_db(list_contract[iter][0]))
    return res_list


def dict_contracts_value(id_agent=None,
                         company_name=None,
                         passport_series=None,
                         passport_id=None,
                         client_name=None,
                         client_surname=None,
                         client_sec_name=None,
                         insurance_type_title=None,
                         insurance_type_short_title=None,
                         insurance_type_capital=None,
                         contract_insurance_amount=None,
                         contract_insurance_payment=None,
                         contract_date_start=None,
                         contract_date_stop=None):
    agent = api_db.get_agent(id_agent=id_agent)

    client = {'name': client_name,
              'surname': client_surname,
              'sec_name': client_sec_name,
              'passport_series': passport_series,
              'passport_id': passport_id}

    company = {'name': company_name}

    insurance_type = {'title': insurance_type_title,
                      'short_title': insurance_type_short_title,
                      'capital': insurance_type_capital}

    agent = {'name': agent[1],
             'surname': agent[2],
             'sec_name': agent[3]}

    data_contract = {'client': client,
                     'company': company,
                     'insurance_type': insurance_type,
                     'agent': agent,
                     'insurance_amount': contract_insurance_amount,
                     'insurance_payment': contract_insurance_payment,
                     'date_start': contract_date_start,
                     'date_stop': contract_date_stop,
                     'idcontract': None}

    return data_contract


def dict_analysis_value(period_month=None,
                        capital_start=None,
                        capital_prediction=None,
                        mdd=None,
                        factor=None,
                        kf=None,
                        kf_prediction=None,
                        profit=None):

    if profit < 0:
        anal = "Убыток"
    else:
        anal = "Прибыль"

    data_analysis = {'date_now': datetime.datetime.now().strftime("%Y-%m-%d"),
                     'date_forecast': (datetime.datetime.now() + datetime.timedelta(days=period_month*30)).strftime("%Y-%m-%d"),
                     'capital_start': capital_start,
                     'capital_prediction': capital_prediction,
                     'mdd': mdd,
                     'profit': profit,
                     'period_month': period_month,
                     'factor': factor,
                     'kf': kf,
                     'kf_prediction': kf_prediction,
                     'anal': anal,}

    return data_analysis


def list_month_period_back(date_start, date_real, par=10):
    res = [date_start.strftime('%Y-%m')]
    delta = date_real - date_start  # timedelta
    if delta.days <= 0:
        return None
    date_iter = date_start
    while date_iter < date_real:
        str_date = date_iter.strftime('%Y-%m')
        if str_date != res[-1]:
            res.append(str_date)
        date_iter = date_iter + datetime.timedelta(days=par)

    return res


def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=300):
    """Создаёт столбчатую диаграмму.
        Принимает данные в виде словаря, подпись для графика,
        названия осей и шаблон подсказки при наведении.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0, end=max(data[y_name]) * 1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Bugs found"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "Days after app deployment"
    plot.xaxis.major_label_orientation = 1
    return plot
