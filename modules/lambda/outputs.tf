output "lambda_function_name" {
  description = "Nombre de la función Lambda creada"
  value       = aws_lambda_function.lambda.function_name
}

output "lambda_function_arn" {
  description = "ARN de la función Lambda creada"
  value       = aws_lambda_function.lambda.arn
}
