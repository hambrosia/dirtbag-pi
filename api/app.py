from datetime import datetime
from datetime import timedelta
import flask
import uuid
import db_manager
import sensor_manager
import soil_stats
import time_manager

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
    # Get readings last 24 hrs
    now = datetime.now()
    last_24_hr = time_manager.get_timestamp_24_hr_ago()
    readings_last_24_hr = db_manager.get_readings_between_timestamps(last_24_hr, now)

    avg_soil_moisture_raw_24 = soil_stats.get_column_average(readings_last_24_hr, 'soilmoisture')
    avg_soil_moisture_percent_24 = sensor_manager.get_soil_moisture_percent(avg_soil_moisture_raw_24)
    avg_soil_temp_24 = round(soil_stats.get_column_average(readings_last_24_hr, 'soiltemp'), 2)
    
    # Generate HTML
    html = "<h1>DirtBag Pi, at your service</h1>"
    html += "<br>Soil Moisture: " + str(soil_moisture_percent) + " Percent" 
    html += "<br>Soil Temperature: " + str(soil_temp) + " Celcius"
    html += "<br>"
    html += "<br>Average Soil Moisture Last 24 Hours: " + str(avg_soil_moisture_percent_24) + "  Percent"
    html += "<br>Average Soil Temperature Last 24 Hours: " + str(avg_soil_temp_24) + " Celcius"
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
