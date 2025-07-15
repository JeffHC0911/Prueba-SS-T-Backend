module "dynamodb" {
  source = "./modules/dynamodb"

  surveys_table_name = "MyApp-Surveys"
}
