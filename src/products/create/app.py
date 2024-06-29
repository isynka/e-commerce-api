import json
import boto3
import uuid
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    if ('body' not in event or event['httpMethod'] != 'POST' or 'title' not in event['body']):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad Request'})
        }
    
    new_product = json.loads(event['body'])
    response = add_product_to_db(new_product)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'A new product was saved successfully in database'})
    }


# Insert a new item into DynamoDB table
def add_product_to_db(new_product):
    
    new_product['uuid'] = str(uuid.uuid1())

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('products-table')
    
    try:
        response = table.put_item(Item=new_product)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response