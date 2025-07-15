import json
import os
import boto3
import logging
from botocore.exceptions import ClientError

# Configurar logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info(f"Evento recibido: {json.dumps(event)}")

        survey_id = None

        # Obtener survey_id de query string
        if event.get('queryStringParameters'):
            survey_id = event['queryStringParameters'].get('survey_id')

        # Si no está en query string, obtener del body
        if not survey_id and event.get('body'):
            body = json.loads(event['body'])
            survey_id = body.get('survey_id')

        if not survey_id:
            logger.warning("survey_id no proporcionado en la petición")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'survey_id is required'})
            }

        pk = f"SURVEY#{survey_id}"
        sk = "METADATA"

        logger.info(f"Buscando ítem con PK={pk} y SK={sk}")

        response = table.get_item(
            Key={
                'PK': pk,
                'SK': sk
            }
        )
        item = response.get('Item')

        if not item:
            logger.info(f"Encuesta con survey_id={survey_id} no encontrada")
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Survey not found'})
            }

        logger.info(f"Encuesta encontrada: {item}")

        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }

    except ClientError as e:
        logger.error(f"ClientError obteniendo encuesta: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
