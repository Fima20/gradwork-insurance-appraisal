import psycopg2
from config import host, user, password, db_name
from russian_names import RussianNames
import api_db
import random
from datetime import datetime, timedelta
import time
from werkzeug.security import generate_password_hash, check_password_hash


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


def create_default_user():
    api_db.add_agent(name="Олег",
                     surname="Смирнов",
                     sec_name="Антонович",
                     login="ad",
                     hash_password=generate_password_hash("ad"),
                     qualification="Специалист первой категории"
                     )


def db_filling_contracts(count=10,
                         KF=0.004254,
                         dif_kf=0.1,
                         max_month=24,
                         min_year=2016,
                         max_year=2022):
    id_agent = 1
    company_name = "ГосСтрах"
    title = "Автострахование ОСАГО"
    short_title = "ОСАГО"
    capital = 14580000

    for i in range(count):

        insurance_amount = random.randint(1000, 99999) * 100
        insurance_payment = insurance_amount * KF + (insurance_amount * KF * random.uniform(-dif_kf, dif_kf))
        date_start = gen_datetime(min_year=min_year, max_year=max_year)
        date_stop = date_start + timedelta(days=30 * random.randint(1, max_month))

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
                                                        capital=capital, )
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


def db_filling_payment(probability=1/600
                       ):
    def str_time_prop(start, end, time_format, prop):
        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))
        ptime = stime + prop * (etime - stime)
        return time.strftime(time_format, time.localtime(ptime))

    all_contracts = api_db.get_contracts()
    id_unit = api_db.getid_default_unit()

    for iter_contract in all_contracts:

        random_probability = random.uniform(0, 1)
        if random_probability < probability:
            id_contract = iter_contract[0]
            date_start = str(iter_contract[8])
            date_stop = str(iter_contract[9])
            date_payment = str_time_prop(date_start, date_stop, '%Y-%m-%d', random.random())
            payment = float(iter_contract[6])

            api_db.add_payment(id_contract=id_contract,
                               id_unit=id_unit,
                               date=date_payment,
                               sum=payment)


