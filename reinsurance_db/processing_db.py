import psycopg2
from config import host, user, password, db_name
from russian_names import RussianNames
import api_db
import random
from datetime import datetime, timedelta


def gen_datetime(min_year=1900, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def rebuild():
    api_db.drop_db()
    api_db.create_tables()
    api_db.add_default_unit()

    str_command = 'SELECT version();'
    api_db.db_command(command=str_command)


def db_filling_contracts():

    num_contracts = 60
    KF = 0.004254
    dif_kf = 0.1
    max_month = 24


    id_agent = 1
    company_name = "ГосСтрах"
    title = "Автострахование ОСАГО"
    short_title = "ОСАГО"
    capital = 14580000

    for i in range(num_contracts):

        insurance_amount = random.randint(1000, 99999)*100
        insurance_payment = insurance_amount*KF+(insurance_amount*KF*random.uniform(-dif_kf, dif_kf))
        date_start = gen_datetime(min_year=2020, max_year=2022)
        date_stop = date_start + timedelta(days=30*random.randint(1,max_month))

        date_start = str(date_start)
        date_stop = str(date_stop)

        id_company = api_db.getid_company(name=company_name)
        if id_company:
            contract_create = api_db.update_company(name=company_name, idcompany=id_company)
        else:
            contract_create = api_db.add_company(name=company_name)
            id_company = api_db.getid_company(name=company_name)

        passport_series = random.randint(100000, 999999)
        passport_id = random.randint(1000, 9999)
        id_client = api_db.getid_client(passport_series=passport_series, passport_id=passport_id)
        people = RussianNames(count=1, output_type='dict').get_batch()[0]
        if id_client:
            contract_create = api_db.update_client(name=people['name'],
                                                   surname=people['surname'],
                                                   sec_name=people['patronymic'],
                                                   passport_series=passport_series,
                                                   passport_id=passport_id,
                                                   idclient=id_client)
        else:
            contract_create = api_db.add_client(name=people['name'],
                                                surname=people['surname'],
                                                sec_name=people['patronymic'],
                                                passport_series=passport_series,
                                                passport_id=passport_id)
            id_client = api_db.getid_client(passport_series=passport_series, passport_id=passport_id)

        id_insurance_type = api_db.getid_insurance_type(title=title, short_title=short_title)
        if id_insurance_type:
            contract_create = api_db.update_insurance_type(title=title,
                                                           short_title=short_title,
                                                           capital=capital,
                                                           idinsurance_type=id_insurance_type)
        else:
            contract_create = api_db.add_insurance_type(title=title,
                                                        short_title=short_title,
                                                        capital=capital,)
            id_insurance_type = api_db.getid_insurance_type(title=title)

        id_unit = api_db.getid_default_unit()

        id_contract = api_db.getid_contract(id_client=id_client)
        if id_contract:
            api_db.update_contract(id_client=id_client,
                                   id_company=id_company,
                                   id_unit=id_unit,
                                   id_insurance_type=id_insurance_type,
                                   id_agent=id_agent,
                                   insurance_amount=insurance_amount,
                                   insurance_payment=insurance_payment,
                                   date_start=date_start,
                                   date_stop=date_stop,
                                   idcontract=id_contract)
        else:
            api_db.add_contract(id_client=id_client,
                                id_company=id_company,
                                id_unit=id_unit,
                                id_insurance_type=id_insurance_type,
                                id_agent=id_agent,
                                insurance_amount=insurance_amount,
                                insurance_payment=insurance_payment,
                                date_start=date_start,
                                date_stop=date_stop)

