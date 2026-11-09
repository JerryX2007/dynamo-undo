import boto3
from botocore.exceptions import ClientError

ENDPOINT = "http://localhost:8000"
REGION = "us-east-1"

ddb = boto3.client("dynamodb", endpoint_url=ENDPOINT, region_name=REGION)
streams = boto3.client("dynamodbstreams", endpoint_url=ENDPOINT, region_name=REGION)
stream_arn = ddb.describe_table(TableName="Products")["Table"]["LatestStreamArn"]
shards = streams.describe_stream(StreamArn=stream_arn)["StreamDescription"]["Shards"]

for shard in shards:
    iterator = streams.get_shard_iterator(StreamArn=stream_arn, ShardId=shard["ShardId"], ShardIteratorType="TRIM_HORIZON")["ShardIterator"]
    try:
        records = streams.get_records(ShardIterator=iterator)["Records"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "TrimmedDataAccessException":
            print("shard expired, skipping")
            continue
        raise

    for r in records:
        d = r["dynamodb"]
        item_pk = d["Keys"]["pk"]["S"]
        ts = int(d["ApproximateCreationDateTime"].timestamp())
        seq = d["SequenceNumber"].zfill(40)

        row = {
            "pk":     {"S": "untagged"},
            "sk":     {"S": f"{str(ts).zfill(12)}#{r['eventID']}"},
            "gsi1pk": {"S": "Products#" + item_pk},
            "gsi1sk": {"S": seq},
            "event_name": {"S": r["eventName"]},
            "item_key":   {"M": d["Keys"]},
            "ts":         {"N": str(ts)},
        }

        if "OldImage" in d:
            row["old_image"] = {"M": d["OldImage"]}
        if "NewImage" in d:
            row["new_image"] = {"M": d["NewImage"]}
        try:
            ddb.put_item(
                TableName="AuditLog",
                Item=row,
                ConditionExpression="attribute_not_exists(pk)",
            )
            print("saved", r["eventName"], item_pk)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                print("duplicate, skipped")
            else:
                raise