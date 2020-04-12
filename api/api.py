from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA
import busio
import flask

# Sensor setup
i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)

# API setup
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Soil Reading Calibration
MIN_MOISTURE = 315
MAX_MOISTURE = 1015 - MIN_MOISTURE

#Convert raw moisture reading to percent
def get_soil_moisture_percent(raw_value: int) -> int:
    percent = ( (raw_value - MIN_MOISTURE ) / MAX_MOISTURE ) * 100
    return percent

# Main endpoint
@app.route('/', methods=['GET'])
def home():
    soil_moisture_raw  = ss.moisture_read()
    soil_moisture_percent = round(get_soil_moisture_percent(soil_moisture_raw), 2)
    soil_temp = round(ss.get_temp(), 2)
    html = "<h1>DirtBag-Pi, at your service</h1>"
    html += "<br>Soil Moisture: " + str(soil_moisture_percent) + " Percent" 
    html += "<br>Soil Temperature: " + str(soil_temp) + " Celcius"
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
