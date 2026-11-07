import boto3

ENDPOINT = "http://localhost:8000"
REGION = "us-east-1"

ddb = boto3.client("dynamodb", endpoint_url=ENDPOINT, region_name=REGION)
streams = boto3.client("dynamodbstreams", endpoint_url=ENDPOINT, region_name=REGION)
stream_arn = ddb.describe_table(TableName="Products")["Table"]["LatestStreamArn"]
shards = streams.describe_stream(StreamArn=stream_arn)["StreamDescription"]["Shards"]

for shard in shards:
    iterator = streams.get_shard_iterator(StreamArn=stream_arn, ShardId=shard["ShardId"], ShardIteratorType="TRIM_HORIZON")["ShardIterator"]
    records = streams.get_records(ShardIterator=iterator)["Records"]

    for r in records:
        print(r["eventName"], r["dynamodb"].get("OldImage"), r["dynamodb"].get("NewImage"))