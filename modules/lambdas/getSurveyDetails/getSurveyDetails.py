import json
import os
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):

    survey_id = None

    # Obtener survey_id desde queryStringParameters o body
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        survey_id = event['queryStringParameters'].get('survey_id')
    if not survey_id and 'body' in event and event['body']:
        try:
            body = json.loads(event['body'])
            survey_id = body.get('survey_id')
        except Exception as e:
            logger.error(f"Error parseando body: {str(e)}")

    if not survey_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'survey_id is required'})
        }

    try:
        pk = f"SURVEY#{survey_id}"
        # Leer ítem de encuesta completo por PK (y SK distinto a RESPONSE#, normalmente SK=SURVEY#principal)
        # Suponemos que encuesta guarda SK: SURVEY#{survey_id}
        response = table.get_item(
            Key={
                'PK': pk,
                'SK': pk
            }
        )

        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Survey not found'})
            }

        # Aquí se asume que item tiene el arreglo item['questions']
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }

    except ClientError as e:
        logger.error(f"Error obteniendo encuesta: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
