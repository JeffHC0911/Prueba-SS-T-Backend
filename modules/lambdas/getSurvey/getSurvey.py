import json
import os
import boto3
import logging
from botocore.exceptions import ClientError

# Configuración básica del logger para CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info(f"Evento recibido: {json.dumps(event)}")
        logger.info(f"Consultando todos los surveys en la tabla: {table_name}")

        # Escanear toda la tabla (sólo para pruebas o tablas pequeñas)
        response = table.scan()
        items = response.get('Items', [])

        logger.info(f"Se recuperaron {len(items)} ítems.")

        return {
            'statusCode': 200,
            'body': json.dumps(items)
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
