import json

import boto3


def post_reading():
    
    client = boto3.client('lambda')
    
    function_name = 'dirtbag-save-soil-reading'
    reading = json.dumps({
	"sensorid": "09e9d5b2-cf8f-4aa2-9f9b-ef9425112291",
	"sensorname": "Matt's Living Room",
	"soilmoisture":999, 
	"soiltemp": "60.07"
    })

    response = client.invoke(
            FunctionName=function_name,
            InvocationType='Event',
            Payload=reading
            )

    print(response)
