"""Render html graph for index"""
from datetime import datetime

import plotly.graph_objects as go

import config.config as config
import definitions
import manager.db_manager as db_manager
import manager.sensor_manager as sensor_manager
import manager.time_manager as time_manager


def plot_month():
    """Render html graph for index"""

    timestamp_month_ago = time_manager.get_timestamp_month_ago()
    timestamp_now = datetime.now()

    readings_last_month = db_manager.get_readings_between_timestamps(timestamp_month_ago, timestamp_now)

    timestamps = [row['timestamp'] for row in readings_last_month]
    moisture_readings = [sensor_manager.get_soil_moisture_percent(row['soilmoisture']) for row in readings_last_month]
    temp_readings = [row['soiltemp'] for row in readings_last_month]

    root_path = definitions.ROOT_DIR
    output_path = str(root_path) + '/static/index.html'

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=moisture_readings, mode='lines', name='Soil Moisture Percent'))
    fig.add_trace(go.Scatter(x=timestamps, y=temp_readings, mode='lines', name='Soil Temperature Celsius'))
    
    template = config.get_configs()['template']
    fig.update_layout(title='DirtBag Pi - Soil Stats', template=template)
    fig.write_html(output_path)    

    print("%s: Updated index.html" % timestamp_now)
