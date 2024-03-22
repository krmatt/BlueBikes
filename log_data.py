import pandas as pd
import time

import gbfs_feeds


def log_station_status(duration_s: int, interval_s: int) -> None:
    start_time = time.monotonic()
    end_time = start_time + duration_s

    while time.monotonic() < end_time:
        station_status_dict = gbfs_feeds.get_feed_dict("station_status")["data"]["stations"]
        station_status_df = pd.DataFrame.from_dict(station_status_dict)

        filename = f"./data/station-status_{time.strftime('%Y-%m-%d_%H%M%S', time.localtime())}.csv"
        station_status_df.to_csv(filename)
        print(f"Recorded {filename}")

        time.sleep(interval_s - ((time.monotonic() - start_time) % interval_s))


def main() -> None:
    log_station_status(300, 60)


if __name__ == "__main__":
    main()
