import psycopg2
from reinsurance_db import layouts
from reinsurance_db.config import host, user, password, db_name
from reinsurance_app import utils


def exception_handling(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as _ex:
        print(f"[ERROR] Error - {_ex}")
    finally:
        pass


def db_connect(func, autocommit=True):
    def wrap(*args, **kwargs):

        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
            )
            connection.autocommit = autocommit

            return func(connection=connection, *args, **kwargs)

        except Exception as _ex:
            print(f"[ERROR][Database][db_connect] Error PostgreSQL - {_ex}")
        finally:
            if connection:
                connection.close()

    return wrap


@db_connect
def create_tables(connection):
    for iter_table in layouts.list_create_tables:
        with connection.cursor() as cursor:
            cursor.execute(iter_table)


@db_connect
def drop_db(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA public CASCADE;")

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA public;")


@db_connect
def db_command(connection, command=""):
    with connection.cursor() as cursor:
        cursor.execute(command)
        return cursor.fetchone()


@db_connect
def add_agent(connection,
              name="",
              surname="",
              sec_name="",
              login="",
              hash_password="",
              qualification=""):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO agent (name, surname, sec_name, login, password, qualification, admin) "
                       f"VALUES ('{name}', '{surname}', '{sec_name}', '{login}', '{hash_password}', '{qualification}', FALSE);")
        # print(f'[INFO][Database] Server: {cursor.fetchone()}')

    return True


@db_connect
def add_default_unit(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO unit (name, small_name) "
                       f"VALUES ('Рубль', 'руб');")

    return True


@db_connect
def getid_default_unit(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT idunit FROM unit WHERE name='Рубль'")
        return cursor.fetchone()[0]


@db_connect
def getid_client(connection, passport_series, passport_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT idclient FROM client WHERE passport_series={passport_series} AND passport_id={passport_id};")
        return cursor.fetchone()[0]


@db_connect
def getid_company(connection, name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT idcompany FROM company WHERE name='{name}';")
        return cursor.fetchone()[0]


@db_connect
def getid_insurance_type(connection, title, short_title):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT idinsurance_type FROM insurance_type WHERE title='{title}' OR short_title='{short_title}';")
        return cursor.fetchone()[0]


@db_connect
def getid_agent(connection, login):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT idagent FROM agent WHERE login='{login}';")
        return cursor.fetchone()[0]


@db_connect
def getid_contract(connection, id_client):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT idcontract FROM contract WHERE id_client={id_client};")
        return cursor.fetchone()[0]


@db_connect
def add_client(connection,
               name="",
               surname="",
               sec_name="",
               passport_series="",
               passport_id=""):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO client (name, surname, sec_name, passport_series, passport_id)"
                       f"VALUES ('{name}', '{surname}', '{sec_name}', {passport_series}, {passport_id});")

    return True


@db_connect
def add_company(connection,
                name=""):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO company (name)"
                       f"VALUES ('{name}');")

    return True


@db_connect
def add_insurance_type(connection,
                       title="",
                       short_title="",
                       capital=""):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO insurance_type (title, short_title, capital)"
                       f"VALUES ('{title}', '{short_title}', '{capital}');")

    return True


@db_connect
def add_contract(connection,
                 id_client="",
                 id_company="",
                 id_unit="",
                 id_insurance_type="",
                 id_agent="",
                 insurance_amount="",
                 insurance_payment="",
                 date_start="",
                 date_stop=""):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO contract (id_client, id_company, id_unit, id_insurance_type, id_agent, "
                       f"insurance_amount, insurance_payment, date_start, date_stop) "
                       f"VALUES ('{id_client}', '{id_company}', '{id_unit}', {id_insurance_type}, {id_agent},  '{insurance_amount}', '{insurance_payment}', '{date_start}', '{date_stop}');")

    return True


@db_connect
def update_client(connection,
                  name="",
                  surname="",
                  sec_name="",
                  passport_series="",
                  passport_id="",
                  idclient=""):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE client SET name='{name}', surname='{surname}', sec_name='{sec_name}',"
                       f" passport_series={passport_series}, passport_id={passport_id} WHERE idclient={idclient};")

    return True


@db_connect
def update_company(connection,
                   name="",
                   idcompany=""):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE company SET name='{name}' WHERE idcompany={idcompany};")

    return True


@db_connect
def update_insurance_type(connection,
                          title="",
                          short_title="",
                          capital="",
                          idinsurance_type=""):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE insurance_type SET title='{title}', short_title='{short_title}', capital={capital} WHERE "
                       f"idinsurance_type={idinsurance_type};")

    return True


@db_connect
def update_contract(connection,
                    id_client="",
                    id_company="",
                    id_unit="",
                    id_insurance_type="",
                    id_agent="",
                    insurance_amount="",
                    insurance_payment="",
                    date_start="",
                    date_stop="",
                    idcontract=""):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE contract SET id_client='{id_client}', id_company='{id_company}', id_unit='{id_unit}', "
                       f"id_insurance_type='{id_insurance_type}', id_agent='{id_agent}', "
                       f"insurance_amount='{insurance_amount}', insurance_payment='{insurance_payment}', date_start='{date_start}', date_stop='{date_stop}' WHERE idcontract={idcontract};")

    return True


@db_connect
def get_contracts(connection):
    cursor = connection.cursor()
    com = f"SELECT * FROM contract;"
    cursor.execute(com)
    contract = cursor.fetchall()
    return contract


@db_connect
def get_client(connection, id_client):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM client WHERE idclient={id_client};")
        return cursor.fetchone()


@db_connect
def get_contract(connection, id_contract):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM contract WHERE idcontract={id_contract};")
        return cursor.fetchone()


@db_connect
def get_company(connection, id_company):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM company WHERE idcompany={id_company};")
        return cursor.fetchone()


@db_connect
def get_insurance_type(connection, id_insurance_type):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM insurance_type WHERE idinsurance_type={id_insurance_type};")
        return cursor.fetchone()


@db_connect
def get_agent(connection, id_agent):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM agent WHERE idagent={id_agent};")
        return cursor.fetchone()


@db_connect
def get_full_contract(connection, id_contract):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * "
                       f"FROM contract, client, company, agent, insurance_type "
                       f"WHERE contract.id_client = client.idclient AND "
                       f"contract.id_company=idcompany AND contract.id_agent=idagent AND "
                       f"contract.id_insurance_type=idinsurance_type AND idcontract={id_contract};")

        return cursor.fetchone()
