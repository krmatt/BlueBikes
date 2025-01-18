"""
Practice creating synthetic controls.
Estimate what the rental and return rates at full/empty stations
would have been if they had more docks/bikes available.

Reference: https://towardsdatascience.com/causal-inference-with-synthetic-control-in-python-4a79ee636325
"""
import datetime
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import analyze_data

matplotlib.use("Agg")


DIR_DATA_RAW = "../data/station-status/raw"
FILE_STATION_INFO = "data/station-information/station_information.csv"
FILE_STATION_STATUS = "../data/station-status/raw/station-status.csv"


def concatenate_data():
    df = pd.DataFrame()

    for file in os.listdir(DIR_DATA_RAW):
        tmp_df = pd.read_csv(f"{DIR_DATA_RAW}/{file}")
        df = pd.concat([df, tmp_df])

    df.to_csv(FILE_STATION_STATUS,
              index=False)


def epoch_to_seconds_since_midnight(epoch_seconds: int):
    dt = datetime.datetime.fromtimestamp(epoch_seconds)
    seconds_since_midnight = (dt.hour * 3600) + (dt.minute * 60) + dt.second
    return seconds_since_midnight


def create_rental_synthetic_control(station_id: str):
    """
    Create a synthetic control for the rental patterns of a given station.
    :param station_id: The ID of the station of interest.
    :return:
    """
    df = pd.read_csv(FILE_STATION_STATUS)
    print(df.info())

    to_keep = ["num_bikes_available",
               "num_docks_available",
               "num_ebikes_available",
               "station_id",
               "last_reported",
               "is_renting",
               "is_returning"]

    one_station_id = "f606593b-3d07-40f2-bc6d-a0eb96588e44"
    one_station_info = analyze_data.get_station_info(one_station_id)

    df = df[to_keep]
    one_station = (df.loc[df["station_id"] == one_station_id]
                   .drop_duplicates(subset=["last_reported"])
                   .sort_values(by="last_reported"))
    one_station["last_reported"] = pd.to_datetime(one_station["last_reported"], unit="s")

    one_station_shifted = one_station.shift(periods=1, axis=0, fill_value=np.nan)
    one_station["rentals"] = (one_station_shifted["num_bikes_available"] - one_station["num_bikes_available"]).clip(lower=0)
    one_station["returns"] = (one_station_shifted["num_docks_available"] - one_station["num_docks_available"]).clip(lower=0)

    one_station["rental_rate"] = (one_station.shift(periods=12, axis=0, fill_value=np.nan)["num_bikes_available"] - one_station["num_bikes_available"])  # rentals/hr

    one_station["last_reported_datetime"] = pd.to_datetime(one_station["last_reported"], unit="s")
    one_station["last_reported_date"] = pd.to_datetime(one_station["last_reported"], unit="s").dt.date
    one_station["time_of_day"] = (one_station["last_reported_datetime"].dt.hour * 3600) + (one_station["last_reported_datetime"].dt.minute * 60) + one_station["last_reported_datetime"].dt.second

    # one_station.plot(x="time_of_day",  # "last_reported",
    #                  y=["rentals", "returns", "rental_rate"],
    #                  kind="line",
    #                  figsize=(50, 5))
    # plt.title(f"Stock at {one_station_info['name'][0]}")
    # plt.xlabel("Time")
    # plt.ylabel("Count")
    # plt.savefig(f"../fig/{one_station_id}.pdf",
    #             bbox_inches="tight")

    daily_df = one_station.groupby("last_reported_date")

    daily_df.plot(kind="line", ax=plt.gca())

    # plt.figure(figsize=(50,5))
    # plt.kind="line"
    #
    # for group in daily_df:
    #     plt.plot(group["time_of_day"],
    #              group["rental_rate"])
    #
    # plt.title("daily df")
    # plt.xlabel("Time of day")
    # plt.ylabel("Rental rate (bikes/hr)")
    plt.savefig("../fig/daily_df.pdf",
                bbox_inches="tight")


if __name__ == "__main__":
    create_rental_synthetic_control("")
    # print(epoch_to_seconds_since_midnight(1718638642))
