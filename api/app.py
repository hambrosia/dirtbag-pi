from datetime import datetime
from datetime import timedelta
import flask
import uuid
import db_manager
import sensor_manager

# API setup
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Main endpoint
@app.route('/', methods=['GET'])
def home() -> None:
    # Create metadata
    reading_uuid = uuid.uuid4()
    reading_timestamp = datetime.now()

    # Get moisture and temperature readings
    soil_moisture_raw  = sensor_manager.get_soil_moisture()
    soil_moisture_percent = sensor_manager.get_soil_moisture_percent(soil_moisture_raw) 
    soil_temp = sensor_manager.get_soil_temp()
    
    # Save reading to database
    db_manager.save_reading(reading_uuid, reading_timestamp, soil_moisture_raw, soil_temp)
    # Print all readings (test)
    all_readings = db_manager.get_all_readings()
    print(all_readings[0][0])

    # Generate HTML
    html = "<h1>DirtBag Pi, at your service</h1>"
    html += "<br>Soil Moisture: " + str(soil_moisture_percent) + " Percent" 
    html += "<br>Soil Temperature: " + str(soil_temp) + " Celcius"
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
