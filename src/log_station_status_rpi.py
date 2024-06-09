import json
import pandas as pd
import time
import requests


URL_STATION_STATUS = "https://gbfs.lyft.com/gbfs/2.3/bos/en/station_status.json"


def log_station_status() -> None:
    data = json.loads(requests.get(URL_STATION_STATUS).text)["data"]["stations"]
    df = pd.DataFrame.from_dict(data)

    filename = f"../data/raw/station-status_{time.strftime('%Y-%m-%d_%H%M', time.localtime())}.csv"
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    log_station_status()
