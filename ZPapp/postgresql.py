import psycopg2
from psycopg2 import OperationalError

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
    if connection is None:
        print("Connection is None. Cannot execute query.")
        return None
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
