resource "aws_dynamodb_table" "surveys_table" {
  name         = var.surveys_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  range_key    = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  attribute {
    name = "entityType"
    type = "S"
  }

  attribute {
    name = "admin_id"
    type = "S"
  }

  attribute {
    name = "survey_id"
    type = "S"
  }

  attribute {
    name = "version_id"
    type = "S"
  }

  attribute {
    name = "respondent_email"
    type = "S"
  }

  attribute {
    name = "created_at"
    type = "S"
  }

  attribute {
    name = "submitted_at"
    type = "S"
  }

  global_secondary_index {
    name            = "GSI1"
    hash_key        = "entityType"
    range_key       = "created_at"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI2"
    hash_key        = "admin_id"
    range_key       = "PK"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI3"
    hash_key        = "survey_id"
    range_key       = "SK"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI4"
    hash_key        = "version_id"
    range_key       = "SK"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI5"
    hash_key        = "respondent_email"
    range_key       = "submitted_at"
    projection_type = "ALL"
  }

  tags = {
    Environment = "dev"
    Project     = "IntelligentSurveySystem"
  }
}
