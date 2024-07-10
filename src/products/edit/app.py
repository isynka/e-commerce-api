import json
import boto3
import decimal
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    if('pathParameters' not in event or event['httpMethod'] != 'PUT'):
        return {
            'statusCode' : 400,
            'body' : json.dumps({'message' : 'Bad Request'})
        }
    
    update_product = json.loads(event['body'])
    payload = event['pathParameters']
    response = update_product_from_db(payload['uuid'], update_product)
    
    return {
        'statusCode' : response['ResponseMetadata']['HTTPStatusCode'],
        'body' : json.dumps({})
    }

def update_product_from_db(uuid, products):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('products-table')

    title = products['title']
    price = products['price']
    description = products['description']

    try:
        response = table.update_item(
            Key={'uuid' : uuid},
            UpdateExpression="SET #title = :title, #price = :price, #description = :description",
            ExpressionAttributeNames={
                "#title": "title",
                "#price": "price",
                "#description": "description"
            },
            ExpressionAttributeValues={
                ":title": title,
                ":price": price,
                ":description": description,
            }
        )

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