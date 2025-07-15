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

        if event.get('queryStringParameters'):
            survey_id = event['queryStringParameters'].get('survey_id')

        if not survey_id and event.get('body'):
            body = json.loads(event['body'])
            survey_id = body.get('survey_id')

        if not survey_id:
            logger.warning("survey_id no proporcionado en la petición")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'survey_id is required'})
            }

        # Construir claves PK y SK según modelo single-table
        pk = f"SURVEY#{survey_id}"
        sk = "METADATA"

        logger.info(f"Intentando eliminar ítem con PK={pk} y SK={sk}")

        response = table.delete_item(
            Key={
                'PK': pk,
                'SK': sk
            },
            ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
        )

        logger.info(f"Encuesta {survey_id} eliminada exitosamente")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Survey {survey_id} deleted successfully'})
        }

    except ClientError as e:
        logger.error(f"ClientError al eliminar encuesta: {e}")
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

    except Exception as e:
        logger.error(f"Error inesperado al eliminar encuesta: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
