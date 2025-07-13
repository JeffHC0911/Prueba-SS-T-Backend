variable "function_name" {
  description = "Nombre de la función Lambda"
  type        = string
}

variable "handler" {
  description = "Handler de la función Lambda (archivo.función)"
  type        = string
}

variable "runtime" {
  description = "Runtime de Lambda"
  type        = string
  default     = "python3.11"
}

variable "filename" {
  description = "Ruta al archivo ZIP con el código Lambda empaquetado"
  type        = string
}

variable "environment_variables" {
  description = "Variables de entorno para Lambda"
  type        = map(string)
  default     = {}
}

variable "dynamodb_actions" {
  description = "Permisos DynamoDB para la política IAM"
  type        = list(string)
  default = [
    "dynamodb:PutItem",
    "dynamodb:GetItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Query",
    "dynamodb:Scan"
  ]
}

variable "dynamodb_resources" {
  description = "ARNs de recursos DynamoDB para la política IAM"
  type        = list(string)
}
