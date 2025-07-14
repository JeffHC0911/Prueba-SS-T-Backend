import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        survey_id = None

        if event.get('queryStringParameters'):
            survey_id = event['queryStringParameters'].get('survey_id')

        if not survey_id and event.get('body'):
            body = json.loads(event['body'])
            survey_id = body.get('survey_id')

        if not survey_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'survey_id is required'})
            }

        # Intentar eliminar el ítem
        response = table.delete_item(
            Key={'survey_id': survey_id},
            ConditionExpression="attribute_exists(survey_id)"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Survey {survey_id} deleted successfully'})
        }

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Survey not found'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
