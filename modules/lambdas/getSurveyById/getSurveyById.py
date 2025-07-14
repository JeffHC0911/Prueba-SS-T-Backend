import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Obtener survey_id desde parámetros query string o body
        survey_id = None

        # Intentar obtener survey_id de query string
        if event.get('queryStringParameters'):
            survey_id = event['queryStringParameters'].get('survey_id')

        # Si no está en query string, intentar del body
        if not survey_id and event.get('body'):
            body = json.loads(event['body'])
            survey_id = body.get('survey_id')

        if not survey_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'survey_id is required'})
            }

        response = table.get_item(Key={'survey_id': survey_id})
        item = response.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Survey not found'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
