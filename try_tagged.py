import boto3
from tagged_table import TaggedTable

ddb = boto3.client("dynamodb", endpoint_url="http://localhost:8000", region_name="us-east-1")

table = TaggedTable(ddb, "Products", change_set="deploy-7")
table.put_item({"pk": {"S": "prod-7"}, "name": {"S": "Glue"}, "price": {"N": "2"}})
print("written")