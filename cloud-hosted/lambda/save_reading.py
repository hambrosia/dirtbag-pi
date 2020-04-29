from datetime import datetime
import json
import uuid

import boto3


def lambda_handler(event, context):
    print("Validating event body")
    # Do some validation here

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('DirtbagReadings')
    body = event['body']
    readings = json.loads(body)
    reading_uuid = str(uuid.uuid4())
    reading_timestamp = str(datetime.now())
    reading_soilmoisture = readings['soilmoisture']
    reading_soiltemp = readings['soiltemp']

    response = table.put_item(
        Item={
            'uuid': reading_uuid,
            'timestamp': reading_timestamp,
            'soilmoisture': reading_soilmoisture,
            'soiltemp': reading_soiltemp
        }
    )

    print("PutItem succeeded:")
    return {
        'statusCode': 200,
        'body': json.dumps(readings)
    }
