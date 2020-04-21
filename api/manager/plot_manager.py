from datetime import datetime

import plotly
from plotly.graph_objs import Layout, Scatter

import manager.db_manager as db_manager
import manager.sensor_manager as sensor_manager
import manager.time_manager as time_manager

def plot_month():

    timestamp_month_ago = time_manager.get_timestamp_month_ago()
    timestamp_now = datetime.now()
 
    readings_last_month = db_manager.get_readings_between_timestamps(timestamp_month_ago, timestamp_now)

    timestamps = [row['timestamp'] for row in readings_last_month]
    moisture_readings = [sensor_manager.get_soil_moisture_percent(row['soilmoisture']) for row in readings_last_month]

    plotly.offline.plot({
        "data": [Scatter(x=timestamps, y=moisture_readings, mode='lines')],
        "layout": Layout(title="DirtBag Pi: Soil Moisture Last 31 Days")},
                        filename='static/index.html')

    print("%s: Updated index.html" % timestamp_now)
