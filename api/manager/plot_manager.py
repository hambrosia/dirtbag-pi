import plotly
from plotly.graph_objs import Scatter, Layout
import manager.db_manager as db_manager
import manager.time_manager as time_manager
from datetime import datetime
import manager.sensor_manager as sensor_manager

def plot_month():

    timestamp_month_ago = time_manager.get_timestamp_month_ago()
    timestamp_now = datetime.now()
    
    readings_last_month = db_manager.get_readings_between_timestamps(timestamp_month_ago, timestamp_now)

    timestamps = [row['timestamp'] for row in readings_last_month]
    moisture_readings = [sensor_manager.get_soil_moisture_percent(row['soilmoisture']) for row in readings_last_month]
    
 
    data = [Scatter(x=timestamps, y=moisture_readings, mode='lines')]
    plotly.offline.plot(data, filename='static/index.html')

    print("Updated index.html")
