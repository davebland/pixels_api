# Pixels API (AWS Lambda Function)

import json
import boto3
from boto3.dynamodb.conditions import Key

# DB Setup
dynamodb = boto3.resource('dynamodb',region_name='eu-west-1')
table = dynamodb.Table('pixels')

def lambda_handler(event, context):
    # Use the request path to select the function & call with either post data (body) or query string
    func = path_function_dict.get(event["requestContext"]["http"]["path"], respond_404)
    if event["requestContext"]["http"]["method"] == "POST":
        return func(event['body'])
    return func(event['rawQueryString'])


def get_all_pixels(*args):
    # Return coordinates & rgba values for all pixels
    try:
        response = table.scan(
            ProjectionExpression="coordinates, rgba"
        )
        return response['Items']
    except Exception as e:
        print(e)
        return {"statusCode":500}

def get_pixel_info(cords):
    # Return all data fields for pixel coordinates given in query string
    try:
        response = table.get_item(
            Key={'coordinates':int(cords)}
        )
        if "Item" in response.keys():
            return response['Item']
        return {"statusCode":404}

    except Exception as e:
        print(e)
        return {"statusCode":500}

def add_pixel(post_data):
    # Record a pixel using the post data
    post_data = json.loads(post_data)
    try:
        response = table.put_item(
        Item={
                'coordinates': post_data['coordinates'],
                'rgba': post_data['rgba'],
            }
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return "Added pixel {}".format(post_data['coordinates'])
        raise Exception(response)
    except Exception as e:
        print(e)
        return {"statusCode":500}
    
def respond_404(*args):
    return {"statusCode":404}

path_function_dict = {
    '/default/pixels/all': get_all_pixels,
    '/default/pixels/data': get_pixel_info,
    '/default/pixels/new': add_pixel,
}

# Test Data
with open("exampleapidata.json") as data:
    test_json = json.loads(data.read())
    print(lambda_handler(test_json,None))