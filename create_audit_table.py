import boto3

ENDPOINT = "http://localhost:8000"
REGION = "us-east-1"

ddb = boto3.client("dynamodb", endpoint_url=ENDPOINT, region_name=REGION)
audit_table = ddb.create_table(
    TableName = "AuditLog",
    BillingMode="PAY_PER_REQUEST",

    AttributeDefinitions=[
        {"AttributeName": "pk", "AttributeType": "S"},
        {"AttributeName": "sk", "AttributeType": "S"},
        {"AttributeName": "gsi1pk", "AttributeType": "S"},
        {"AttributeName": "gsi1sk", "AttributeType": "S"}
    ],

    KeySchema=[
        {"AttributeName": "pk", "KeyType": "HASH"},
        {"AttributeName": "sk", "KeyType": "RANGE"}
    ],

    GlobalSecondaryIndexes=[
        {
            "IndexName": "by-item",
            "KeySchema": [
                {"AttributeName": "gsi1pk", "KeyType": "HASH"},
                {"AttributeName": "gsi1sk", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"},
        }
    ],
)

print("created")