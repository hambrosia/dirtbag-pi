from decimal import *
import json

import boto3


def lambda_handler(event, context):
    print("Validating event body")
    # Do some validation here

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

    print("PutItem succeeded:")
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
