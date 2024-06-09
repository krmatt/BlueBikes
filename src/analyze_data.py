import os

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")


DIR_DATA_RAW = "data/station-status/rpi-raw"


def concat_data():
    df = pd.DataFrame()

    to_drop = ["is_installed",
               "is_returning",
               "eightd_has_available_keys",
               "legacy_id",
               "num_docks_disabled",
               "num_scooters_unavailable",
               "num_scooters_available",
               "num_docks_available",
               "num_bikes_disabled"]

    for file in os.listdir(DIR_DATA_RAW):
        tmp_df = pd.read_csv(f"{DIR_DATA_RAW}/{file}")
        tmp_df.drop(columns=to_drop, inplace=True)

        df = pd.concat([df, tmp_df])

    df.to_csv("data/station-status/cleaned/station-status.csv", index=False)


def analyze_time_series():
    df_all = pd.read_csv("../data/station-status/cleaned/station-status.csv")
    df_one = df_all.loc[df_all["station_id"] == "4b5de733-9353-4873-9dc2-9558b3cb063a"]



    to_drop = ["is_renting",
               "station_id"]

    df_one.drop(columns=to_drop, inplace=True)

    df_one.plot(type="line")
    plt.savefig("fig/myplot.pdf")


def analyze_station_data():
    filepath = ""
    stations = pd.read_csv(filepath)

    to_drop = [
        "is_installed",
        "is_returning",
        "eightd_has_available_keys",
        "legacy_id",
        "num_docks_disabled",
        "num_scooters_unavailable",
        "num_scooters_available",
        "num_docks_available",
        "last_reported",
        "num_bikes_disabled",
        "station_id",
        "num_ebikes_available",
        "num_bikes_available"
    ]
    stations.drop(columns=to_drop, inplace=True)
    for column in stations.columns:
        print(column)

    print(stations.loc[stations["is_renting"] == 0])

    stations.plot(kind="hist")
    plt.savefig("fig/myplot.pdf")


def plot_station_stock_over_time(station_ids: list[str]) -> None:
    """
    Plot the number of available bikes and docks at each station over time.
    :param station_ids: The IDs of the stations to use.
    :return: None
    """
    to_keep = [
        "station_id",
        # "is_renting",
        # "is_returning",
        "num_bikes_available",
        "num_ebikes_available",
        "num_bikes_disabled",
        "num_docks_available",
        "num_docks_disabled",
        "last_reported"
    ]

    df_full = organize_data(DIR_DATA_RAW)
    df = df_full[to_keep]

    for station_id in station_ids:
        df_station = df.loc[df["station_id"] == station_id].copy()
        df_station.drop_duplicates(subset="last_reported",
                                   keep="first",
                                   inplace=True)
        df_station.sort_values(by="last_reported",
                               inplace=True)
        df_station["last_reported"] = (pd.to_datetime(df_station["last_reported"], unit="s"))

        df_station["docks_plus_bikes"] = df_station["num_bikes_available"] + df_station["num_docks_available"]

        station_info = get_station_info(station_id)

        df_station.plot(x="last_reported",
                        y=[
                            "num_bikes_available",
                            "num_ebikes_available",
                            "num_docks_available",
                            "docks_plus_bikes",
                            "num_docks_disabled",
                            "num_bikes_disabled"
                        ],
                        kind="line")
        plt.title(f"Stock at {station_info['name'][0]}")
        plt.xlabel("Time (mm-dd HH)")
        plt.ylabel("Count")
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.savefig(f"fig/{station_id}_stock.pdf", bbox_inches="tight")


def organize_data(directory) -> pd.DataFrame:
    """
    Concatenate data from CSVs in a directory into a single dataframe.
    :param directory: The directory that contains the CSVs to concatenate.
    :return: A concatenated DataFrame.
    """
    df_list = [pd.read_csv(os.path.join(directory, file)) for file in os.listdir(directory)]
    df_concat = pd.concat(df_list)

    return df_concat


def get_station_info(station_id: str) -> dict:
    """
    Get the information about a station.
    :param station_id: The unique ID number of the station.
    :return: A dict of information about the station.
    """
    station_info_df = pd.read_csv("data/station-information/station_information.csv")
    return station_info_df.loc[station_info_df["station_id"] == station_id].to_dict(orient="list")


if __name__ == "__main__":
    plot_station_stock_over_time(["f834a67b-0de8-11e7-991c-3863bb43a7d0"])
    # print(get_station_info("800bde2c-51df-497c-ac2d-bc3a8c00c164"))
