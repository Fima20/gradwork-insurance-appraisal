import psycopg2
from config import host, user, password, db_name
import processing_db
import api_db

processing_db.rebuild()
processing_db.create_default_user()
processing_db.db_filling_contracts(count=1000, KF=0.05)
processing_db.db_filling_payment(probability=1/300)
# print(api_db.get_full_contract(id_contract=30))

