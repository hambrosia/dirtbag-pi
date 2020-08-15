"""Post readings to Lambda for processing"""
from datetime import datetime
import json

import boto3

from ..config import config

CONFIGS = config.get_configs()


def post_reading(sensor_id: str, sensor_name: str, timestamp: str, soil_moisture: int, soil_temp: float):
    """Takes sensor id, sensor name, soil moisture, and temp and sends to AWS Lambda, logs response to console"""

    client = boto3.client('lambda')
    function_name = CONFIGS['lambda-function-name']

    reading = json.dumps({
        "timestamp": timestamp,
        "sensorid": sensor_id,
        "sensorname": sensor_name,
        "soilmoisture": soil_moisture,
        "soiltemp": str(soil_temp)
    })

    response = client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=reading
    )

    timestamp = datetime.now()
    print(
        "%s: Soil reading sent, response status code: %s" % (timestamp, response['ResponseMetadata']['HTTPStatusCode']))
