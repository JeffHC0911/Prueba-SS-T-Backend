import json
import os
import boto3
from boto3.dynamodb.conditions import Attr
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info(f"Evento recibido: {json.dumps(event)}")
        logger.info(f"Consultando todos los surveys en la tabla: {table_name}")

        # Scan con FilterExpression para traer solo los ítems donde entityType=='Survey'
        response = table.scan(
            FilterExpression=Attr('entityType').eq('Survey')
        )
        items = response.get('Items', [])

        logger.info(f"Se recuperaron {len(items)} ítems filtrados como encuestas.")

        return {
            'statusCode': 200,
            'body': json.dumps(items),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except ClientError as e:
        logger.error(f"ClientError al escanear la tabla: {str(e)}")
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
