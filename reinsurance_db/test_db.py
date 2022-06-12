import psycopg2
from config import host, user, password, db_name
import processing_db
import api_db

processing_db.rebuild()
processing_db.create_default_user()
processing_db.db_filling_contracts(count=2000)
processing_db.db_filling_payment(probability=1/600)
# print(api_db.get_full_contract(id_contract=30))


# try:
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=db_name,
#     )
#     connection.autocommit = True
#
#     # cursor = connection.cursor()
#     # with connection.cursor() as cursor:
#     #     cursor.execute('')
#     #     print(f'Server version: {cursor.fetchone()}')
#
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT version();')
#         print(f'Server: {cursor.fetchone()}')
#
#     # with connection.cursor() as cursor:
#     #     cursor.execute("""INSERT INTO insurance_type (title, short_title) VALUES (
#     #     'Обязательное страхование автогражданской ответственности (Стандарт)', 'ОСАГО(стандарт)');""")
#     #     print(f'Server accept')
#
#     # with connection.cursor() as cursor:
#     #     cursor.execute("""ALTER TABLE insurance_type ALTER COLUMN short_title SET DATA TYPE VARCHAR(15);""")
#     #     print(f'Server accept')
#
# except Exception as _ex:
#     print(f"[INFO] Error PostgreSQL - {_ex}")
# finally:
#     if connection:
#         connection.close()
#         print("[INFO] PostgreSQL connection closed")
