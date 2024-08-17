"""
Practice creating synthetic controls.
Estimate what the rental and return rates at full/empty stations
would have been if they had more docks/bikes available.

Reference: https://towardsdatascience.com/causal-inference-with-synthetic-control-in-python-4a79ee636325
"""
import os

import matplotlib
import pandas as pd

import analyze_data

matplotlib.use("Agg")


DIR_DATA_RAW = "../data/station-status/raw"
FILE_STATION_INFO = "data/station-information/station_information.csv"


def concatenate_data():
    df = pd.DataFrame()

    for file in os.listdir(DIR_DATA_RAW):
        tmp_df = pd.read_csv(f"{DIR_DATA_RAW}/{file}")
        df = pd.concat([df, tmp_df])

    df.to_csv("../data/station-status/raw/station-status.csv",
              index=False)


def create_rental_synthetic_control(station_id: str):
    """
    Create a synthetic control for the rental patterns of a given station.
    :param station_id: The ID of the station of interest.
    :return:
    """
    pass


if __name__ == "__main__":
    pass
