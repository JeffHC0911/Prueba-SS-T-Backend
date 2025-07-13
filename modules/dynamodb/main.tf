resource "aws_dynamodb_table" "surveys" {
  name         = var.surveys_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "survey_id"

  attribute {
    name = "survey_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "survey_versions" {
  name         = var.survey_versions_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "version_id"

  attribute {
    name = "version_id"
    type = "S"
  }

  attribute {
    name = "survey_id"
    type = "S"
  }

  global_secondary_index {
    name            = "survey_id-index"
    hash_key        = "survey_id"
    projection_type = "ALL"
  }
}

resource "aws_dynamodb_table" "questions" {
  name         = var.questions_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "question_id"

  attribute {
    name = "question_id"
    type = "S"
  }

  attribute {
    name = "version_id"
    type = "S"
  }

  global_secondary_index {
    name            = "version_id-index"
    hash_key        = "version_id"
    projection_type = "ALL"
  }
}

resource "aws_dynamodb_table" "responses" {
  name         = var.responses_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "response_id"

  attribute {
    name = "response_id"
    type = "S"
  }

  attribute {
    name = "version_id"
    type = "S"
  }

  global_secondary_index {
    name            = "version_id-index"
    hash_key        = "version_id"
    projection_type = "ALL"
  }
}

resource "aws_dynamodb_table" "answers" {
  name         = var.answers_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "answer_id"

  attribute {
    name = "answer_id"
    type = "S"
  }

  attribute {
    name = "response_id"
    type = "S"
  }

  global_secondary_index {
    name            = "response_id-index"
    hash_key        = "response_id"
    projection_type = "ALL"
  }
}

resource "aws_dynamodb_table" "files" {
  name         = var.files_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "file_id"

  attribute {
    name = "file_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "templates" {
  name         = var.templates_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "template_id"

  attribute {
    name = "template_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "template_questions" {
  name         = var.template_questions_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "template_question_id"

  attribute {
    name = "template_question_id"
    type = "S"
  }

  attribute {
    name = "template_id"
    type = "S"
  }

  global_secondary_index {
    name            = "template_id-index"
    hash_key        = "template_id"
    projection_type = "ALL"
  }
}
