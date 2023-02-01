variable "def_region" {
  type    = string
  default = "us-east-2"
}

variable "result" {

  type    = string
  default = "erjan-result"
}

variable "vote" {
  type    = string
  default = "erjan-vote"
}


variable "account_id" {
  type    = string
  default = "025416187662"
}


variable "dynamodb_table_name" {
  type    = string
  default = "votes"

}

variable "dynamodb_partition_key" {
  type    = string
  default = "voter"

}

variable "dynamodb_field" {
  type    = string
  default = "vote"
}

variable "sns_name" {
  type    = string
  default = "erjan_sns"

}


variable "sqs_name" {
  type    = string
  default = "erjan_sqs"

}


variable "apigateway_name" {
  type    = string
  default = "apigateway-vote"

}
