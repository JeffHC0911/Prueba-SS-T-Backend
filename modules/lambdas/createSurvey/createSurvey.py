import json
import os
import boto3
import uuid
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Generar survey_id si no viene en el body
        survey_id = body.get('survey_id') or f"survey-{uuid.uuid4().hex[:8]}"
        
        title = body.get('title')
        if not title:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'title is required'})
            }

        item = {
            'survey_id': survey_id,
            'title': title,
            'description': body.get('description', ''),
            'admin_id': body.get('admin_id', ''),
            'branding': body.get('branding', {}),
            'template_id': body.get('template_id', None),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }

        table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(survey_id)'
        )

        return {
            'statusCode': 201,
            'body': json.dumps(item)
        }

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 409,
                'body': json.dumps({'message': 'Survey already exists'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
