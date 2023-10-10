import psycopg2
from psycopg2 import OperationalError
import json
from ZPapp.config import settings

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection()


def get_coord(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def get_coord_store(db):
    select_coord = f"SELECT address, latitude, longitude FROM {db}"
    coord = get_coord(connection, select_coord)
    return coord

# def get_coord_wfm():
#     select_tj_coord = "SELECT latitude, longitude FROM wfm"
#     data_tj = get_coord(connection, select_tj_coord)
#     return data_tj


# def create_database(connection, query):
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Query executed successfully")
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")

# create_database_query = "CREATE DATABASE sm_app"
# create_database(connection, create_database_query)

# def execute_query(connection, query):
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Query executed successfully")
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")

################################################################################################
# Создание таблицы и заполнение данными из JSON
# create_table = """
# DROP TABLE IF EXISTS tj;
# CREATE TABLE IF NOT EXISTS tj (
#   id SERIAL PRIMARY KEY,
#   address TEXT,
#   latitude FLOAT,
#   longitude FLOAT
# );
# """

# execute_query(connection, create_table)

# with open('./ZPapp/DataStores/T_J_stores_coord.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# for item in data:
#     if "'" in item[0]:
#         item[0] = item[0].replace("'", "`")
#     insert_query = (
#         f"INSERT INTO tj (address, latitude, longitude) VALUES {item[0], item[1], item[2]}"
#     )
#     connection.autocommit = True
#     cursor = connection.cursor()
#     cursor.execute(insert_query, item)
################################################################################################

# Заполнение таблицы WFM

# with open('./ZPapp/DataStores/WFM_stores_coord.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# for item in data:
#     if "'" in item[0]:
#         item[0] = item[0].replace("'", "`")
#     insert_query = (
#         f"INSERT INTO wfm (address, latitude, longitude) VALUES {item[0], item[1], item[2]}"
#     )

#     connection.autocommit = True
#     cursor = connection.cursor()
#     cursor.execute(insert_query, item)
################################################################################################


