"""Manager for database functions: connect, return rows between timestamps, save rows, read sensor and write row, return column average """

import os
import sys
import uuid
from datetime import datetime

import psycopg2
import psycopg2.extras

import config.config as config
import manager.sensor_manager as sensor_manager

# Postgres setup
DB_CONFIG = config.get_configs()['db-config']
try:
    CONN = psycopg2.connect(DB_CONFIG)
except:
    print("Unable to connect to database, verify database configuration and credentials")
    sys.exit(os.EX_CONFIG)
CUR = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
psycopg2.extras.register_uuid()


def get_readings_between_timestamps(timestamp_start: datetime, timestamp_end: datetime):
    """Return readings between two timestamps in order to display graph for week, month, etc """

    query = """
    SELECT timestamp, soilmoisture, soiltemp
    FROM readings
    WHERE timestamp BETWEEN %s AND %s
    """
    values = (timestamp_start, timestamp_end)
    CUR.execute(query, values)
    return CUR.fetchall()


def write_reading(reading_uuid: str, reading_timestamp: datetime, soilmoisture: float, soiltemp: float) -> None:
    """Save a row to the database with a uuid, timestamp, moisture reading, and temp reading"""

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
    """Reads moisture and temp from sensor, saves to new row in database"""

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
    """Returns average value for column/list"""

    total = 0
    if not soil_readings:
        return 0
    for row in soil_readings:
        total += row[column]
    avg = total / len(soil_readings)
    return avg
