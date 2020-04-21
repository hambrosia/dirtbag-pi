import os
import sys
import uuid
from datetime import datetime

import psycopg2
import psycopg2.extras

import manager.sensor_manager as sensor_manager

# Postgres setup
DB_CONFIG = 'dbname=dirtbag'
try:
    CONN = psycopg2.connect(DB_CONFIG)
except:
    print("Unable to connect to database, verify database configuration and credentials")
    sys.exit(os.EX_CONFIG)
CUR = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
psycopg2.extras.register_uuid()

def get_readings_between_timestamps(timestamp_start: datetime, timestamp_end: datetime):
    query = """
    SELECT timestamp, soilmoisture, soiltemp
    FROM readings
    WHERE timestamp BETWEEN %s AND %s
    """
    values = (timestamp_start, timestamp_end)
    CUR.execute(query, values)
    return CUR.fetchall()

def write_reading(reading_uuid: str, reading_timestamp: datetime, soilmoisture: float, soiltemp: float) -> None:
    query = """
    INSERT INTO
        readings
    VALUES
        (%s, %s, %s, %s)
    """
    values = (reading_uuid, reading_timestamp, soilmoisture, soiltemp)
    CUR.execute(query, values)
    CONN.commit()

def take_and_write_reading():
    # Create metadata
    reading_uuid = uuid.uuid4()
    reading_timestamp = datetime.now()

    # Get moisture and temperature readings
    soil_moisture_raw = sensor_manager.get_soil_moisture()
    soil_moisture_percent = sensor_manager.get_soil_moisture_percent(soil_moisture_raw)
    soil_temp = sensor_manager.get_soil_temp()

    # Save reading to database
    write_reading(reading_uuid, reading_timestamp, soil_moisture_raw, soil_temp)
    print("%s: Saved reading to database" % reading_timestamp)

def get_column_average(soil_readings: list, column: str) -> float:
    total = 0
    if not soil_readings:
        return 0
    for row in soil_readings:
        total += row[column]
    avg = total / len(soil_readings)
    return avg
