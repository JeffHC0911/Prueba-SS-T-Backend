import json
import os
import boto3
import logging
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info(f"Evento recibido: {json.dumps(event)}")

        body = json.loads(event.get('body', '{}'))

        survey_id = body.get('survey_id')
        respondent_id = body.get('respondent_id')  # ID del encuestado, opcional
        answers = body.get('answers')  # La estructura con las respuestas
        metadata = body.get('metadata', {})

        if not survey_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'survey_id is required'})
            }
        if not answers:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'answers are required'})
            }

        response_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        pk = f"SURVEY#{survey_id}"
        sk = f"RESPONSE#{response_id}"

        item = {
            'PK': pk,
            'SK': sk,
            'entityType': 'Response',
            'survey_id': survey_id,
            'response_id': response_id,
            'respondent_id': respondent_id,
            'answers': answers,
            'metadata': metadata,
            'created_at': now
        }

        logger.info(f"Ingresando respuesta: {item}")

        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Response created', 'response_id': response_id})
        }

    except ClientError as e:
        logger.error(f"ClientError creando respuesta: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error(f"Error inesperado creando respuesta: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
