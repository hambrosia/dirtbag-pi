from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA
import busio
from datetime import datetime
import flask
import psycopg2
import psycopg2.extras
import uuid

# Sensor setup
i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)

# API setup
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Soil reading calibration
MIN_MOISTURE = 315
MAX_MOISTURE = 1015 - MIN_MOISTURE 

# Convert raw moisture reading to percent
def get_soil_moisture_percent(raw_value: int) -> float:
    percent = ( (raw_value - MIN_MOISTURE ) / MAX_MOISTURE ) * 100
    return percent

# Postgres setup
db_config = 'dbname=dirtbag user=pi'
conn = psycopg2.connect(db_config)
cur = conn.cursor()
psycopg2.extras.register_uuid()

def save_reading(reading_uuid: str, reading_timestamp: str, soilmoisture: float, soiltemp: float) -> None:
    query = """
    INSERT INTO
        readings
    VALUES
        (%s, %s, %s, %s)
    """
    values = (reading_uuid, reading_timestamp, soilmoisture, soiltemp)
    print("Saved values to db")
    cur.execute(query, values)
    conn.commit()

# Main endpoint
@app.route('/', methods=['GET'])
def home() -> None:
    # Create metadata
    reading_uuid = uuid.uuid4()
    reading_timestamp = datetime.now()
    
    # Get moisture and temperature readings
    soil_moisture_raw  = ss.moisture_read()
    soil_moisture_percent = round(get_soil_moisture_percent(soil_moisture_raw), 2)
    soil_temp = round(ss.get_temp(), 2)
    
    # Save reading to database
    save_reading(reading_uuid, reading_timestamp, soil_moisture_raw, soil_temp)
    
    # Generate HTML
    html = "<h1>DirtBag Pi, at your service</h1>"
    html += "<br>Soil Moisture: " + str(soil_moisture_percent) + " Percent" 
    html += "<br>Soil Temperature: " + str(soil_temp) + " Celcius"
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
