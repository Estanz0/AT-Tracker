import sys
sys.path.append("/Users/byron-mac/MyDocuments/Projects/AT-Bus/server_py")

import requests
# import pandas as pd
import json 

import config

from sqlalchemy import inspect, MetaData
from database import engine

AT_API_GTFS = "https://api.at.govt.nz/v2/gtfs/"
MY_API = "http://127.0.0.1:8000"


AT_HEADER = {
    # Request headers
    'Ocp-Apim-Subscription-Key': config.AT_API_KEY,
}

def update():
    update_table(table='routes')
    update_table(table='trips')
    update_stops() 
    # update_routes()
    # update_trips()
    # update_stops() 
    # update_stop_times()

def update_table(table):
    """
    Updates a table using data retrieved from AT API.
    Can be used for tables with one primary key column.
        - Create / Update records 
        - Delete records
    """

    base_at_url = f'{AT_API_GTFS}/{table}/'
    base_my_url = f'{MY_API}/{table}/'

    # Create, update records
    column_names = get_column_names(table)
    primary_key = get_primary_key(table)
    response = requests.get(base_at_url, headers=AT_HEADER)
    records = response.json()["response"]

    for i, rec in enumerate(records):
        # filter and reorder columns to match schema
        rec = {key: rec[key] for key in column_names}
        data = json.dumps(rec)
        res = requests.post(base_my_url, data=data)

    # Delete records
    # Find existing records that no longer exist
    existing_ids = get_existing_records(table, primary_key)
    updated_ids = [rec[primary_key] for rec in records]
    ids_to_delete = [rec_id for rec_id in existing_ids if rec_id not in updated_ids]
    for rec_id in ids_to_delete:
        res = requests.delete(f'{base_my_url}{rec_id}')

def update_stops():
    """
    Update the stops table
        - Update stop_id of existing stops
        - Delete removed stops
        - Create new stops
    """
    table = 'stops'
    secondary_table = 'routes'

    base_at_url = f'{AT_API_GTFS}/{table}/'
    base_at_url_secondary = f'{AT_API_GTFS}/{table}/tripId/'
    base_my_url = f'{MY_API}/{table}/'
    base_my_url_secondary = f'{MY_API}/{secondary_table}/'


    # Create, update records
    column_names = get_column_names(table)
    primary_key = get_primary_key(table)
    records_all = []

    response_secondary_db = requests.get(base_my_url_secondary)
    for ir, rec_secondary in enumerate(response_secondary_db.json()):
        if rec_secondary['trips']:
            trip_id = rec_secondary['trips'][0]['trip_id']
            response = requests.get(f'{base_at_url_secondary}{trip_id}', headers=AT_HEADER)
            records = response.json()["response"]

            for i, rec in enumerate(records):
                records_all.append(rec)
                # filter and reorder columns to match schema
                rec = {key: rec[key] for key in column_names}
                rec['route_id'] = rec_secondary['route_id']
                data = json.dumps(rec)
                res = requests.post(base_my_url, data=data)
        print(f'Stops created: {len(records_all)}')
        print(f'Routes processed: {ir}')

    # Delete records
    # Find existing records that no longer exist
    records = records_all
    existing_ids = get_existing_records(table, primary_key)
    updated_ids = [rec[primary_key] for rec in records]
    ids_to_delete = [rec_id for rec_id in existing_ids if rec_id not in updated_ids]
    for rec_id in ids_to_delete:
        res = requests.delete(f'{base_my_url}{rec_id}')


    

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