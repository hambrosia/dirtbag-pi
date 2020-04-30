from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key, Attr


def get_timestamp_month_ago():
    """Return a timestamp 31 days prior to the present time"""
    month_delta = timedelta(days=31)
    return datetime.now() - month_delta


def lambda_handler(event, context):
    # Should be triggered on table update. Will use sensor id
    # Return readings between timestamps (boto3)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DirtbagReadings')
    timestamp_now = str(datetime.now())
    timestamp_one_month_ago = str(get_timestamp_month_ago())

    response = table.query(
        KeyConditionExpression=Key('sensorid').eq('09e9d5b2-cf8f-4aa2-9f9b-ef9425112291') & Key('timestamp').between(
            timestamp_one_month_ago, timestamp_now)
    )

    for i in response['Items']:
        print(i)

    # Organize for graph
    # Make index.html (plotly)
    # Save to S3 (boto3)

    return {
        'statusCode': 200,
        'body': ""
    }
