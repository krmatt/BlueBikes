import boto3
import json
import os
import time
import urllib3


TABLE_NAME = "bluebikes_station_status"
TIMEZONE = "America/New_York"
URL_STATION_STATUS = "https://gbfs.lyft.com/gbfs/2.3/bos/en/station_status.json"


def get_station_status() -> list:
    http = urllib3.PoolManager()
    return json.loads(http.request("GET", URL_STATION_STATUS).data)["data"]["stations"]


def lambda_handler(event: any, context: any) -> dict:
    os.environ["TZ"] = TIMEZONE
    time.tzset()

    db = boto3.resource("dynamodb")
    table = db.Table(TABLE_NAME)

    timestamp = f"{time.strftime('%Y-%m-%d_%H%M%S', time.localtime())}"
    table.put_item(Item={"timestamp": timestamp,
                         "stations": get_station_status()})

    return {"message": f"Logged station status at {timestamp}."}


if __name__ == "__main__":
    print(lambda_handler({}, None))
