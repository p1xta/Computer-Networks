from pydantic import BaseModel

import psycopg2


class Car(BaseModel):
    name : str
    price : str 
    year : str
    mileage : str
    engine_capacity : str
    horse_powers : str
    fuel_type : str
    transmission : str
    car_type : str
    drive : str
    color : str

def get_db_connection():
    with open('config.txt', 'r') as config_file:
        user = config_file.readline()[:-1]
        password = config_file.readline()

    DB_CONFIG = {
    "dbname": "parsed_site",
    "user": user,
    "password": password,
    "host": "localhost",
    "port": "5432",
    "client_encoding": "UTF8"
}
    return psycopg2.connect(**DB_CONFIG)

def save_to_db(data):
    conn = get_db_connection()
    conn.set_client_encoding('UTF8')
    cursor = conn.cursor()

    for entry in data:
        cursor.execute("""
            INSERT INTO cars (name, price, year, mileage, engine_capacity, horse_powers, fuel_type, transmission, car_type, drive, color)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            entry['name'], entry['price'], entry['year'], entry['mileage'],
            entry['engine_capacity'], entry['horse_powers'], entry['fuel_type'],
            entry['transmission'], entry['car_type'], entry['drive'], entry['color']
        ))

    conn.commit()
    cursor.close()
    conn.close()

def get_all_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM cars;""")
    result = cursor.fetchall()
    return result