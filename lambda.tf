module "create_survey_lambda" {
  source = "./modules/lambda"

  function_name = "createSurvey"
  handler       = "createSurvey.lambda_handler"  # archivo createSurvey.py, función lambda_handler
  runtime       = "python3.11"
  filename      = "modules/lambdas/createSurvey/createSurvey.zip"

  environment_variables = {
    SURVEYS_TABLE_NAME = module.dynamodb.surveys_table_name
  }

  dynamodb_actions = [
    "dynamodb:PutItem",
    "dynamodb:GetItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Query",
    "dynamodb:Scan"
  ]

  dynamodb_resources = [
    module.dynamodb.surveys_table_arn
  ]
}
