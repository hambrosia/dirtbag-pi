from datetime import datetime
from datetime import timedelta
import flask
import uuid
import manager.db_manager as db_manager
import manager.sensor_manager as sensor_manager
import manager.time_manager as time_manager
import manager.plot_manager as plot_manager
from apscheduler.schedulers.background import BackgroundScheduler

# Write readings to database every 15 mins
def update_db_and_html():
    db_manager.take_and_write_reading()
    plot_manager.plot_month()

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_db_and_html, trigger="interval", minutes=1)
scheduler.start()

# API setup
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Main endpoint
@app.route('/', methods=['GET'])
def home() -> None:

    # Get moisture and temperature readings
    soil_moisture_raw  = sensor_manager.get_soil_moisture()
    soil_moisture_percent = sensor_manager.get_soil_moisture_percent(soil_moisture_raw) 
    soil_temp = sensor_manager.get_soil_temp()
    
    # Get readings last 24 hrs
    now = datetime.now()
    last_24_hr = time_manager.get_timestamp_24_hr_ago()
    readings_last_24_hr = db_manager.get_readings_between_timestamps(last_24_hr, now)

    avg_soil_moisture_raw_24 = db_manager.get_column_average(readings_last_24_hr, 'soilmoisture')
    avg_soil_moisture_percent_24 = sensor_manager.get_soil_moisture_percent(avg_soil_moisture_raw_24)
    avg_soil_temp_24 = round(db_manager.get_column_average(readings_last_24_hr, 'soiltemp'), 2)
    
    # Generate HTML
    html = "<h1>DirtBag Pi, at your service</h1>"
    html += "<br>Soil Moisture: " + str(soil_moisture_percent) + " Percent" 
    html += "<br>Soil Temperature: " + str(soil_temp) + " Celcius"
    html += "<br>"
    html += "<br>Average Soil Moisture Last 24 Hours: " + str(avg_soil_moisture_percent_24) + "  Percent"
    html += "<br>Average Soil Temperature Last 24 Hours: " + str(avg_soil_temp_24) + " Celcius"
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')
