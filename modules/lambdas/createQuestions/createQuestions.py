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
        question_id = body.get('question_id')

        if not survey_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'survey_id is required'})
            }

        if not question_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'question_id is required'})
            }

        now = datetime.utcnow().isoformat()

        pk = f"SURVEY#{survey_id}"
        sk = f"QUESTION#{question_id}"

        item = {
            'PK': pk,
            'SK': sk,
            'entityType': 'Question',
            'survey_id': survey_id,
            'question_id': question_id,
            'text': body.get('text', ''),
            'type': body.get('type', 'text'),  # ejemplo: text, choice, multiple-choice
            'options': body.get('options', []), # para preguntas con opciones tipo choice
            'created_at': now,
            'updated_at': now
        }

        logger.info(f"Insertando pregunta: {item}")

        table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(PK) AND attribute_not_exists(SK)'  # no sobrescribir
        )

        return {
            'statusCode': 201,
            'body': json.dumps(item)
        }

    except ClientError as e:
        logger.error(f"Error creando pregunta: {str(e)}")
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 409,
                'body': json.dumps({'message': 'La pregunta ya existe'})
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
