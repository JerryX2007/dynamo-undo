class TaggedTable:
    def __init__(self, client, table_name, change_set):
        self.client = client
        self.table_name = table_name
        self.change_set = change_set

    def put_item(self, item):
        tagged = dict(item)
        tagged["_cs"] = {"S": self.change_set}
        return self.client.put_item(TableName=self.table_name, Item=tagged)
        
