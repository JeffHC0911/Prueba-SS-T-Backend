module "dynamodb" {
  source = "./modules/dynamodb"

  surveys_table_name           = "MyApp-Surveys"
  survey_versions_table_name   = "MyApp-SurveyVersions"
  questions_table_name         = "MyApp-Questions"
  responses_table_name         = "MyApp-Responses"
  answers_table_name           = "MyApp-Answers"
  files_table_name             = "MyApp-Files"
  templates_table_name         = "MyApp-Templates"
  template_questions_table_name = "MyApp-TemplateQuestions"
}
