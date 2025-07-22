import json
import os
import boto3
import logging
from datetime import datetime
from botocore.exceptions import ClientError

# Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SURVEYS_TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info(f"Evento recibido: {event}")
        
        body = json.loads(event.get('body', '{}'))
        survey_id = body.get('survey_id')
        new_status = body.get('status')
        start_date = body.get('start_date')  # ISO 8601 string
        end_date = body.get('end_date')      # ISO 8601 string

        # Validar entrada
        if not survey_id or not new_status:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'message': 'survey_id y status son requeridos'}),
            }

        valid_statuses = ['borrador', 'publicado', 'archivado', 'cerrado']
        if new_status not in valid_statuses:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'message': f'status inválido. Valores permitidos: {valid_statuses}'})
            }

        pk = f"SURVEY#{survey_id}"
        sk = "METADATA"

        # Construir expresión de actualización dinámica
        update_expr = "SET #s = :status, updated_at = :updated_at"
        expr_attr_vals = {
            ':status': new_status,
            ':updated_at': datetime.utcnow().isoformat()
        }
        expr_attr_names = {
            '#s': 'status'
        }

        if start_date:
            update_expr += ", start_date = :start_date"
            expr_attr_vals[':start_date'] = start_date

        if end_date:
            update_expr += ", end_date = :end_date"
            expr_attr_vals[':end_date'] = end_date

        response = table.update_item(
            Key={'PK': pk, 'SK': sk},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_attr_vals,
            ExpressionAttributeNames=expr_attr_names,
            ReturnValues="ALL_NEW"
        )

        logger.info(f"Respuesta de DynamoDB: {response}")

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': f'Encuesta {survey_id} actualizada a estado {new_status}',
                'updated_item': response.get('Attributes')
            })
        }

    except ClientError as e:
        logger.error(f"ClientError: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al actualizar la encuesta', 'details': str(e)})
        }

    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error inesperado', 'details': str(e)})
        }
