import sys
sys.path.append("/Users/byron-mac/MyDocuments/Projects/AT-Bus/server_py")

import requests, zipfile, io
import json, csv
import sqlite3
import pandas

import config

from sqlalchemy import inspect, MetaData
from database import engine

MY_API = "http://127.0.0.1:8000"

def download_gtfs_files():
    r = requests.get('https://cdn01.at.govt.nz/data/gtfs.zip')
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("./data")

def update():
    print("Downloading ZIP File ...", end=" ")
    download_gtfs_files()
    print("Completed")

    table_names = [
        'routes',
        'shapes',
        'trips',
        'stops',
        'stop_times'
    ]

    for table_name in table_names:
        print(f'Updating table {table_name} ...', end=" ")
        replace_table(table=table_name)
        print("Completed")

def replace_table(table):
    conn = create_connection(r'../at_bus_app.db')

    df = pandas.read_csv(f'./data/{table}.txt')
    df.to_sql(table, conn, if_exists='replace', index=False)


def create_connection(db_file):
    """ 
    create a database connection to the SQLite database specified by the db_file

    :param db_file: database file
    :return: Connection object or None
    """

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def get_column_names(table_name):
    inspector = inspect(engine)
    column_descs = inspector.get_columns(table_name)
    column_names = [x['name'] for x in column_descs]
    return column_names

def get_primary_key(table_name):
    inspector = inspect(engine)
    column_descs = inspector.get_columns(table_name)
    for col in column_descs:
        if col['primary_key'] == 1:
            return col['name']
    return None

def get_existing_records(table_name, column_name):
    response = requests.get(f'{MY_API}/{table_name}')
    ids = [x[column_name] for x in response.json()]
    return ids
    

if __name__ == "__main__":
    update()