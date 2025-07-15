module "create_survey_lambda" {
  source = "./modules/lambda"

  function_name = "createSurvey"
  handler       = "createSurvey.lambda_handler"
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

module "get_survey_lambda" {
  source = "./modules/lambda"

  function_name = "getSurvey"
  handler       = "getSurvey.lambda_handler"
  runtime       = "python3.11"
  filename      = "modules/lambdas/getSurvey/getSurvey.zip"

  environment_variables = {
    SURVEYS_TABLE_NAME = module.dynamodb.surveys_table_name
  }

  dynamodb_actions = [
    "dynamodb:GetItem",
    "dynamodb:Scan"
  ]

  dynamodb_resources = [
    module.dynamodb.surveys_table_arn
  ]
}

module "get_survey_by_id_lambda" {
  source = "./modules/lambda"

  function_name = "getSurveyById"
  handler       = "getSurveyById.lambda_handler"
  runtime       = "python3.11"
  filename      = "modules/lambdas/getSurveyById/getSurveyById.zip"

  environment_variables = {
    SURVEYS_TABLE_NAME = module.dynamodb.surveys_table_name
  }

  dynamodb_actions = [
    "dynamodb:GetItem",
    "dynamodb:Scan"
  ]

  dynamodb_resources = [
    module.dynamodb.surveys_table_arn
  ]
}

module "delete_survey_lambda" {
  source = "./modules/lambda"

  function_name = "deleteSurvey"
  handler       = "deleteSurvey.lambda_handler"
  runtime       = "python3.11"
  filename      = "modules/lambdas/deleteSurvey/deleteSurvey.zip"

  environment_variables = {
    SURVEYS_TABLE_NAME = module.dynamodb.surveys_table_name
  }

  dynamodb_actions = [
    "dynamodb:DeleteItem"
  ]

  dynamodb_resources = [
    module.dynamodb.surveys_table_arn
  ]
}



