from datetime import datetime
import json

import boto3


def post_reading(sensor_id: str, sensor_name: str, soil_moisture: int, soil_temp: float):
    
    client = boto3.client('lambda')
    
    function_name = 'dirtbag-save-soil-reading'
    reading = json.dumps({
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
    print("%s: Soil reading sent, response status code: %s" % (timestamp, response['ResponseMetadata']['HTTPStatusCode']))
