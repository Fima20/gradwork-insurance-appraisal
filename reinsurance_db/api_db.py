import psycopg2
from reinsurance_db import layouts
from reinsurance_db.config import host, user, password, db_name


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
        print(f'[INFO][Database] Server: {cursor.fetchone()}')

    return True




