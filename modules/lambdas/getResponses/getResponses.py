import json
import os
import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# Configurar logger para CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info(f"Evento recibido: {json.dumps(event)}")

        survey_id = None

        # Obtener survey_id desde query string
        if event.get('queryStringParameters'):
            survey_id = event['queryStringParameters'].get('survey_id')

        # Si no está en query string, intentar del body
        if not survey_id and event.get('body'):
            body = json.loads(event['body'])
            survey_id = body.get('survey_id')

        if not survey_id:
            logger.warning("survey_id no proporcionado")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'survey_id is required'})
            }

        pk = f"SURVEY#{survey_id}"

        logger.info(f"Consultando respuestas con PK={pk}")

        # Query usando KeyConditionExpression para PK y filtro begins_with en SK
        response = table.query(
            KeyConditionExpression=Key('PK').eq(pk) & Key('SK').begins_with('RESPONSE#')
        )

        items = response.get('Items', [])

        logger.info(f"Encontradas {len(items)} respuestas")

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }

    except ClientError as e:
        logger.error(f"Error ClientError consultando respuestas: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error(f"Error inesperado consultando respuestas: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
