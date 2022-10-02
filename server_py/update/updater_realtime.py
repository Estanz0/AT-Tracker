import sys
sys.path.append("/Users/byron-mac/MyDocuments/Projects/AT-Bus/server_py")

import requests
# import pandas as pd
import json 
import time

import config

from sqlalchemy import inspect, MetaData
from database import engine

AT_API_GTFS = "https://api.at.govt.nz/v2/public/realtime"
MY_API = "http://127.0.0.1:8000"


AT_HEADER = {
    # Request headers
    'Ocp-Apim-Subscription-Key': config.AT_API_KEY,
}

def update():
    update_vehicle_positions()

def update_vehicle_positions():
    table = 'vehicle_positions'

    base_at_url = f'{AT_API_GTFS}/vehiclelocations/'
    base_my_url = f'{MY_API}/{table}/'

    # Create, update records
    column_names = get_column_names(table)
    primary_key = get_primary_key(table)
    response = requests.get(base_at_url, headers=AT_HEADER)
    records = response.json()['response']['entity']

    for i, rec in enumerate(records):
        # filter and reorder columns to match schema
        rec = extract_data(rec)
        rec = {key: rec[key] for key in column_names}
        data = json.dumps(rec)
        # print(data)
        res = requests.post(base_my_url, data=data)

    # Delete records
    # Find existing records that no longer exist
    existing_ids = get_existing_records(table, primary_key)
    updated_ids = [rec['id'] for rec in records]
    ids_to_delete = [rec_id for rec_id in existing_ids if rec_id not in updated_ids]
    for rec_id in ids_to_delete:
        res = requests.delete(f'{base_my_url}{rec_id}')

def extract_data(rec):
    new_rec = dict()
    new_rec['vehicle_id'] = rec['id']

    vehicle_rec = rec.get('vehicle', dict())

    new_rec['vehicle_timestamp'] = vehicle_rec.get('timestamp', None)

    trip_rec = vehicle_rec.get('trip', dict())
    new_rec['trip_id'] = trip_rec.get('trip_id', None)
    new_rec['route_id'] = trip_rec.get('route_id', None)
    new_rec['direction_id'] = trip_rec.get('direction_id', None)
        
    position_rec = vehicle_rec.get('position', dict())
    new_rec['vehicle_lat'] = position_rec.get('latitude', None)
    new_rec['vehicle_lon'] = position_rec.get('longitude', None)
    new_rec['vehicle_bearing'] = position_rec.get('bearing', None)
    new_rec['vehicle_speed'] = position_rec.get('speed', None)

    return new_rec

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
