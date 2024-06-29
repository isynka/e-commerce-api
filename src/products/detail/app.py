import json
import boto3
import decimal
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    if('pathParameters' not in event or event['httpMethod'] != 'GET'):
        return {
            'statusCode' : 400,
            'body' : json.dumps({'message' : 'Bad Request'})
        }
    
    payload = event['pathParameters']

    response = get_product_from_db(payload['uuid'])

    if('Item' not in response):
        return {
            'statusCode' : 404,
            'body' : json.dumps({'message' : 'Product not found'})
        }
    
    return {
        'statusCode' : 200,
        'body' : json.dumps(response['Item'], indent=2, default=handle_decimal_type)
    }


def get_product_from_db(uuid):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('products-table')

    try:
        response = table.get_item(Key={'uuid' : uuid})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

def handle_decimal_type(obj):
    if isinstance(obj, decimal.Decimal):
        if float(obj).is_integer():
            return int(obj)
        else:
            return float(obj)
    raise TypeError