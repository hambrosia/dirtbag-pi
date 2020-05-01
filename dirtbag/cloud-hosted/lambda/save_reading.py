from datetime import datetime
from decimal import *
import json

import boto3


def lambda_handler(event, context):
    print("Validating event body")
    # Do some validation here

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('DirtbagReadings')
    body = event['body']
    readings = json.loads(body)

    reading_timestamp = str(datetime.now())
    sensor_id = readings['sensorid']
    sensor_name = readings['sensorname']
    reading_soilmoisture = readings['soilmoisture']
    reading_soiltemp = Decimal(readings['soiltemp'])

    response = table.put_item(
        Item={
            'sensorid': sensor_id,
            'timestamp': reading_timestamp,
            'sensorname': sensor_name,
            'soilmoisture': reading_soilmoisture,
            'soiltemp': reading_soiltemp
        }
    )

    print("PutItem succeeded:")
    return {
        'statusCode': 200,
        'body': json.dumps(readings)
    }
