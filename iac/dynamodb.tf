


# ###########################################
# # dynamodb table creation
# ###########################################

resource "aws_dynamodb_table" "dynamodb_table_votes" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = var.dynamodb_partition_key

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = var.dynamodb_partition_key
    type = "S"
  }


}


resource "aws_dynamodb_table_item" "item1" {
  table_name = aws_dynamodb_table.dynamodb_table_votes.name
  hash_key   = aws_dynamodb_table.dynamodb_table_votes.hash_key

  item = <<ITEM
{
  "${var.dynamodb_partition_key}": {"S": "count"},
  "a": {"N": "0"},
  "b": {"N": "0"}

}
ITEM
}