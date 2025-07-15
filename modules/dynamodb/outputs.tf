output "surveys_table_name" {
  value = aws_dynamodb_table.surveys_table.name
}

output "surveys_table_arn" {
  value = aws_dynamodb_table.surveys_table.arn
}
