from datetime import timedelta
from datetime import datetime
import psycopg2
import psycopg2.extras

# Postgres setup
db_config = 'dbname=dirtbag'
conn = psycopg2.connect(db_config)
cur = conn.cursor()
psycopg2.extras.register_uuid()

# Prepare intervals for average calculations
def get_week_ago():
    week_delta = timedelta(days = 7)
    return datetime.now() - week_delta

def get_month_ago():
    month_delta = timedelta(days = 31)
    return datetime.now() - month_delta

def get_average_last_week():
    pass

def get_average_last_31_days():
    pass

def save_reading(reading_uuid: str, reading_timestamp: str, soilmoisture: float, soiltemp: float) -> None:
    query = """
    INSERT INTO
        readings
    VALUES
        (%s, %s, %s, %s)
    """
    values = (reading_uuid, reading_timestamp, soilmoisture, soiltemp)
    cur.execute(query, values)
    conn.commit()

