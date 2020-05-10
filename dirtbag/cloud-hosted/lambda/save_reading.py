from decimal import *
import json

import boto3


def validate_body(event, keys) -> bool:
    """Validate event body has all required keys and they are non-null, boundary check
    Return: True (event body valid), False (invalid body)
    """
    for key in keys:
        if key not in event:
            return False
        if event[key] is None:
            return False

    if event['soiltemp'] > 100 or event['soiltemp'] < -100:
        return False

    if event['soilmoisture'] > 2000 or event['soilmoisture'] < 200:
        return False


def lambda_handler(event, context):
    """Validate event body, save to database"""

    print("Validating event body")
    keys = ['timestamp', 'sensorid', 'sensorname', 'soilmoisture', 'soiltemp']
    body_valid = validate_body(event=event, keys=keys)
    if not body_valid:
        return {
            'statusCode': 400,
            'body': json.dumps(event)
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DirtbagReadings')

    reading_timestamp = event['timestamp']
    sensor_id = event['sensorid']
    sensor_name = event['sensorname']
    reading_soilmoisture = event['soilmoisture']
    reading_soiltemp = Decimal(event['soiltemp'])

    response = table.put_item(
        Item={
            'sensorid': sensor_id,
            'timestamp': reading_timestamp,
            'sensorname': sensor_name,
            'soilmoisture': reading_soilmoisture,
            'soiltemp': reading_soiltemp
        }
    )

    print("Saved soil reading to database")
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
