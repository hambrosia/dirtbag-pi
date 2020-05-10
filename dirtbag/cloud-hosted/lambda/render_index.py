from datetime import datetime, timedelta
import os

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import plotly.graph_objects as go

# Soil reading calibration
MIN_MOISTURE = 315
MAX_MOISTURE = 1015 - MIN_MOISTURE


def get_timestamp_month_ago() -> datetime:
    """Return a timestamp 31 days prior to the present time"""
    month_delta = timedelta(days=31)
    return datetime.now() - month_delta


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


def lambda_handler(event, context):
    """Gets recent readings from database, prepares as html graph with Plotly, saves to S3"""

    # Get recent readings from database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DirtbagReadings')
    timestamp_now = str(datetime.now())
    timestamp_one_month_ago = str(get_timestamp_month_ago())
    sensor_id = event['Records'][0]['dynamodb']['Keys']['sensorid']['S']

    response = table.query(
        KeyConditionExpression=Key('sensorid').eq(sensor_id) & Key('timestamp').between(
            timestamp_one_month_ago, timestamp_now)
    )

    # Prepare readings for display as graph
    readings_last_month = response['Items']
    timestamps = [row['timestamp'] for row in readings_last_month]
    moisture_readings = [get_soil_moisture_percent(row['soilmoisture']) for row in readings_last_month]
    temp_readings = [row['soiltemp'] for row in readings_last_month]

    # Render graph, save to /tmp
    output_path = '/tmp/index.html'
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=moisture_readings, mode='lines', name='Soil Moisture Percent'))
    fig.add_trace(go.Scatter(x=timestamps, y=temp_readings, mode='lines', name='Soil Temperature Celsius'))
    fig.update_layout(title='DirtBag Pi - Soil Stats', template='plotly')
    fig.write_html(output_path)

    # Save graph to S3 (boto3)
    s3_client = boto3.client('s3')
    bucket_name = os.environ['OUTPUT_BUCKET']
    file_name = "/tmp/index.html"
    object_name = "index.html"

    # Use put_file instead of put_object to enable multipart transfer
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    # Set content-type to text/html to enable viewing directly in browser
    s3 = boto3.resource('s3')
    api_client = s3.meta.client
    response = api_client.copy_object(Bucket=bucket_name,
                                      Key=object_name,
                                      ContentType="text/html",
                                      MetadataDirective="REPLACE",
                                      CopySource=bucket_name + "/" + object_name)
    print(event)
    return
