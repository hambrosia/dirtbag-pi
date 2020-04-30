from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key, Attr


def get_timestamp_month_ago():
    """Return a timestamp 31 days prior to the present time"""
    month_delta = timedelta(days=31)
    return datetime.now() - month_delta


def lambda_handler(event, context):
    # Return readings between timestamps (boto3)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DirtbagReadings')
    timestamp_now = str(datetime.now())
    timestampe_one_month_ago = str(get_timestamp_month_ago())

    response = table.query(
        KeyConditionExpression=Key('timestamp').between(timestampe_one_month_ago, timestamp_now)
    )

    print(response)

    # Organize for graph
    # Make index.html (plotly)
    # Save to S3 (boto3)

    return {
        'statusCode': 200,
        'body': ""
    }
