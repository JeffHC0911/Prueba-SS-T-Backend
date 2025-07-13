variable "surveys_table_name" {
  type        = string
  description = "Nombre de la tabla Surveys"
  default     = "Surveys"
}

variable "survey_versions_table_name" {
  type        = string
  description = "Nombre de la tabla SurveyVersions"
  default     = "SurveyVersions"
}

variable "questions_table_name" {
  type        = string
  description = "Nombre de la tabla Questions"
  default     = "Questions"
}

variable "responses_table_name" {
  type        = string
  description = "Nombre de la tabla Responses"
  default     = "Responses"
}

variable "answers_table_name" {
  type        = string
  description = "Nombre de la tabla Answers"
  default     = "Answers"
}

variable "files_table_name" {
  type        = string
  description = "Nombre de la tabla Files"
  default     = "Files"
}

variable "templates_table_name" {
  type        = string
  description = "Nombre de la tabla Templates"
  default     = "Templates"
}

variable "template_questions_table_name" {
  type        = string
  description = "Nombre de la tabla TemplateQuestions"
  default     = "TemplateQuestions"
}
