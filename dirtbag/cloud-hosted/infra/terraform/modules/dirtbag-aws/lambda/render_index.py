import logging
import os
from datetime import datetime, timedelta

import boto3
import plotly.graph_objects as go
import pytz
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from pytz import timezone

# Soil reading calibration
MIN_MOISTURE = 315
MAX_MOISTURE = 1015 - MIN_MOISTURE


def get_timestamp_month_ago(timestamp: datetime) -> datetime:
    """Return a timestamp 31 days prior to the provided time"""
    month_delta = timedelta(days=31)
    return timestamp - month_delta


def get_soil_moisture_percent(raw_value: int) -> float:
    """Convert raw soil moisture reading to percent """
    if raw_value == 0:
        return 0
    percent = ((raw_value - MIN_MOISTURE) / MAX_MOISTURE) * 100

    if percent > 100:
        percent = 100
    if percent < 0:
        percent = 0

    return round(percent, 2)


def render_graph_html(timestamps, moisture_readings, temp_readings, timestamp_local) -> None:
    """Render graph, save to /tmp """
    output_path = '/tmp/index.html'
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=moisture_readings, mode='lines', name='Soil Moisture Percent'))
    fig.add_trace(go.Scatter(x=timestamps, y=temp_readings, mode='lines', name='Soil Temperature Celsius'))
    fig.update_layout(title=f'DirtBag Pi - Soil Stats - {timestamp_local}', template='plotly')
    fig.write_html(output_path)


def save_graph_to_bucket(s3_client, file_name, bucket_name, object_name, path):
    """Use put_file instead of put_object to enable multipart transfer"""
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return str(e)
    # Set content-type to text/html to enable viewing directly in browser
    s3 = boto3.resource('s3')
    api_client = s3.meta.client

    object_name = f"{path}/index.html"

    response = api_client.copy_object(Bucket=bucket_name,
                                      Key=object_name,
                                      ContentType="text/html",
                                      MetadataDirective="REPLACE",
                                      CopySource=bucket_name + "/" + object_name)
    return response


def lambda_handler(event, context):
    """Gets recent readings from database, prepares as html graph with Plotly, saves to S3"""

    # Get recent readings from database
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get('TABLE_NAME')
    table = dynamodb.Table(table_name)
    datetime_now = datetime.now(tz=pytz.utc)
    timestamp_one_month_ago = str(get_timestamp_month_ago(datetime_now))
    timestamp_utc = str(datetime_now)

    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    timestamp_local = str(datetime_now.astimezone(timezone('US/Pacific')).strftime(fmt))
    sensor_id = str(event['Records'][0]['dynamodb']['Keys']['sensorid']['S'])

    response = table.query(
        KeyConditionExpression=Key('sensorid').eq(sensor_id) & Key('timestamp').between(
            timestamp_one_month_ago, timestamp_utc)
    )

    # Prepare readings for display as graph
    readings_last_month = response['Items']
    timestamps = [row['timestamp'] for row in readings_last_month]
    moisture_readings = [get_soil_moisture_percent(row['soilmoisture']) for row in readings_last_month]
    temp_readings = [row['soiltemp'] for row in readings_last_month]

    render_graph_html(timestamps=timestamps, moisture_readings=moisture_readings, temp_readings=temp_readings,
                      timestamp_local=timestamp_local)

    res = save_graph_to_bucket(s3_client=boto3.client('s3'), bucket_name=os.environ['OUTPUT_BUCKET'],
                         file_name="/tmp/index.html", path='public')
    print(res)
