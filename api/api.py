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

@app.route('/', methods=['GET'])
def home():
    moisture_reading = ss.moisture_read()
    return "<h1>Dirtbag-Pi, at your service.</h1></br>Moisture: " + str(moisture_reading)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
