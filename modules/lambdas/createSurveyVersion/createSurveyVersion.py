import json
import os
import boto3
import logging
from botocore.exceptions import ClientError
from datetime import datetime

# Configurar logger para CloudWatch
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
        version_number = body.get('version_number')

        if not survey_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'survey_id is required'})
            }

        if not version_number:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'version_number is required'})
            }

        now = datetime.utcnow().isoformat()

        pk = f"SURVEY#{survey_id}"
        sk = f"VERSION#{version_number}"

        item = {
            'PK': pk,
            'SK': sk,
            'entityType': 'SurveyVersion',
            'survey_id': survey_id,
            'version_number': version_number,
            # Puedes agregar más atributos según necesidad:
            'created_at': now,
            'updated_at': now,
            'content': body.get('content', {}),  # Por ejemplo, contenido de la versión
            'notes': body.get('notes', '')
        }

        logger.info(f"Insertando ítem: {item}")

        table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(PK) AND attribute_not_exists(SK)'  # evita sobrescribir versiones existentes
        )

        return {
            'statusCode': 201,
            'body': json.dumps(item)
        }

    except ClientError as e:
        logger.error(f"ClientError al crear versión encuesta: {str(e)}")
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 409,
                'body': json.dumps({'message': 'Esta versión ya existe para la encuesta'})
            }
        else:
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
