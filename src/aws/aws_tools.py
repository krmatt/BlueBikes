import boto3
import pandas as pd
import time

import pandas.errors
from dynamodb_json import json_util


def export_dynamodb_to_csv(table_name: str, limit: int, last_evaluated_key: dict = None) -> None:
    dynamodb = boto3.client("dynamodb")

    if last_evaluated_key:
        response = dynamodb.scan(
            TableName=table_name,
            Select="ALL_ATTRIBUTES",
            ExclusiveStartKey=last_evaluated_key
        )
    else:
        response = dynamodb.scan(
            TableName=table_name,
            Select="ALL_ATTRIBUTES"
        )

    ddb_data = response["Items"]

    responses = 0
    while response.get("LastEvaluatedKey") and responses < limit:
        response = dynamodb.scan(
            TableName=table_name,
            Select="ALL_ATTRIBUTES",
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        ddb_data.extend(response["Items"])
        json_data = json_util.loads(ddb_data)

        try:
            existing_data_df = pd.read_csv("../../data/station-status/db/station_status.csv")
        except pandas.errors.EmptyDataError:
            existing_data_df = pd.DataFrame()
        new_data_df = pd.DataFrame(data=json_data)
        concatenated_data_df = pd.concat([existing_data_df, new_data_df])
        concatenated_data_df.drop_duplicates(subset="timestamp", inplace=True)

        concatenated_data_df.to_csv("data/station-status/db/station_status.csv", index=False)
        responses += 1
        print(f"Recorded response {responses}. {len(concatenated_data_df)} total unique timestamps recorded. Last evaluated key: {response['LastEvaluatedKey']}")


if __name__ == "__main__":
    export_dynamodb_to_csv("bluebikes_station_status", 1000, {'timestamp': {'S': '2024-05-10_035525'}})
