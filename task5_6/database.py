import os

import psycopg2


def get_db_connection():
    DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "client_encoding": "UTF8"
}
    return psycopg2.connect(**DB_CONFIG)

def save_to_db(url : str):
    conn = get_db_connection()
    conn.set_client_encoding('UTF8')
    cursor = conn.cursor()

    cursor.execute(""" INSERT INTO urls (url) VALUES (%s); """, (url, ) )

    conn.commit()
    cursor.close()
    conn.close()

def get_all_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM urls;""")
    result = cursor.fetchall()
    return result