import boto3

client = boto3.client("dynamodb", endpoint_url="http://localhost:8000", region_name="us-east-1")
client.put_item(TableName="Products", Item={"pk": {"S": "prod-2"}, "name": {"S": "Eraser"}, "price": {"N": "0.5"}})
response = client.get_item(TableName="Products", Key={"pk": {"S": "prod-2"}})

print(response)