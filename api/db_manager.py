import datetime
import os
import sys
import psycopg2
import psycopg2.extras

# Postgres setup
db_config = 'dbname=dirtbag'
try:
    conn = psycopg2.connect(db_config)
except:
    print("Unable to connect to database, verify database configuration and credentials")
    sys.exit(os.EX_CONFIG)
cur = conn.cursor()
psycopg2.extras.register_uuid()

def get_readings_between_timestamps(timestamp_start: datetime, timestamp_end: datetime):
    query = """
    SELECT timestamp, soilmoisture, soiltemp
    FROM readings
    WHERE timestamp BETWEEN %s AND %s
    """
    values = (timestamp_start, timestamp_end)
    cur.execute(query, values)
    return cur.fetchall()

def save_reading(reading_uuid: str, reading_timestamp: datetime, soilmoisture: float, soiltemp: float) -> None:
    query = """
    INSERT INTO
        readings
    VALUES
        (%s, %s, %s, %s)
    """
    values = (reading_uuid, reading_timestamp, soilmoisture, soiltemp)
    cur.execute(query, values)
    conn.commit()

