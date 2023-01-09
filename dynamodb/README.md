# DynamoDB

## Данные

* type: on demand
* table name: `Votes` (you can use your own.)
* Partition key: `voter` (string you can use your own.)

The application does not use database migrations, so please add the following entry to the table yourself:

```
{
  "voter": {
    "S": "count"
  },
  "a": {
    "N": "0"
  },
  "b": {
    "N": "0"
  }
}
```
