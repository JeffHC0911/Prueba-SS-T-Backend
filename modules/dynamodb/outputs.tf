output "surveys_table_name" {
  value = aws_dynamodb_table.surveys.name
}

output "survey_versions_table_name" {
  value = aws_dynamodb_table.survey_versions.name
}

output "questions_table_name" {
  value = aws_dynamodb_table.questions.name
}

output "responses_table_name" {
  value = aws_dynamodb_table.responses.name
}

output "answers_table_name" {
  value = aws_dynamodb_table.answers.name
}

output "files_table_name" {
  value = aws_dynamodb_table.files.name
}

output "templates_table_name" {
  value = aws_dynamodb_table.templates.name
}

output "template_questions_table_name" {
  value = aws_dynamodb_table.template_questions.name
}
