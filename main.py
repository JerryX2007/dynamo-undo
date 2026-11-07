import boto3

# TODO: create a low-level DynamoDB client.
# It needs the service name ("dynamodb"), endpoint_url pointing at your
# local copy, and region_name="us-east-1".
client = boto3.client("dynamodb", endpoint_url="http://localhost:8000", region_name="us-east-1")

# TODO: put a second product.
# client.put_item takes TableName=... and Item=...
# Item uses the same typed format as the CLI, but as a Python dict, not a JSON string:
#   {"pk": {"S": "prod-2"}, ...}
client.put_item(TableName="Products", Item={"pk": {"S": "prod-2"}, "name": {"S": "Eraser"}, "price": {"N": "0.5"}})

# TODO: get it back.
# client.get_item takes TableName=... and Key=... (only "pk" is needed)
response = client.get_item(TableName="Products", Key={"pk": {"S": "prod-2"}})

print(response)