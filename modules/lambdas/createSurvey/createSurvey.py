import json
import os
import boto3
import uuid
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
        logger.info(f"Evento recibido: {event}")
        #logger.info(f"Contexto: {event['headers']['authorization']}")

        body = json.loads(event.get('body', '{}'))
        
        # Obtener claims del usuario autenticado
        claims = event.get("requestContext", {}).get("authorizer", {}).get("jwt", {}).get("claims", {})
        admin_id = claims.get("sub") or claims.get("cognito:username")

        logger.info(f"Claims del usuario: {claims}")


        if not admin_id:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Unauthorized: admin_id no encontrado en token'})
            }
        
        # Generar survey_id si no viene en el body
        survey_id = body.get('survey_id') or f"{uuid.uuid4().hex[:8]}"
        
        title = body.get('title')
        if not title:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'title is required'})
            }

        now = datetime.utcnow().isoformat()

        pk = f"SURVEY#{survey_id}"
        sk = "METADATA"

        item = {
            'PK': pk,
            'SK': sk,
            'entityType': 'Survey',
            'survey_id': survey_id,
            'title': title,
            'description': body.get('description', ''),
            'admin_id': admin_id,
            'branding': body.get('branding', {}),
            'template_id': body.get('template_id', None),
            'created_at': now,
            'updated_at': now
        }

        logger.info(f"Guardando ítem: {item}")

        table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(PK) AND attribute_not_exists(SK)'
        )

        return {
            'statusCode': 201,
            'body': json.dumps(item)
        }

    except ClientError as e:
        logger.error(f"ClientError: {e}")
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
        logger.error(f"Error inesperado: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
