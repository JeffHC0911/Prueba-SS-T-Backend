import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Escanear toda la tabla (ten cuidado con tablas grandes)
        response = table.scan()
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
