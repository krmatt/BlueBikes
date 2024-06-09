import json

import pandas
import pandas as pd
import requests
import time


def get_feeds() -> dict:
    """
    Get a dict of the available GBFS feed names and URLs.
    :return: The available GBFS feed names and URLs.
    """
    gbfs_feeds_list = json.loads(requests.get("https://gbfs.bluebikes.com/gbfs/gbfs.json").text)["data"]["en"]["feeds"]
    gbfs_feeds_dict = {}
    for feed in gbfs_feeds_list:
        gbfs_feeds_dict[feed["name"]] = feed["url"]

    return gbfs_feeds_dict


def get_feed_dict(feed_name: str) -> dict:
    """
    Get the JSON data for a feed as a dict.
    :param feed_name: The name of the GBFS data feed to get.
    :return: The latest data from the feed.
    """
    feeds = get_feeds()

    if feed_name not in feeds.keys():
        raise ValueError(f"Invalid feed name. Use one of the following feeds: {feeds.keys()}")

    return json.loads(requests.get(feeds[feed_name]).text)


def get_feed_df(feed_name: str) -> pandas.DataFrame:
    """
    Get the JSON data for a feed as a DataFrame.
    :param feed_name: The name of the GBFS feed to get.
    :return: The latest data from the feed.
    """
    feeds = get_feeds()

    if feed_name not in feeds.keys():
        raise ValueError(f"Invalid feed name. Use one of the following feeds: {feeds.keys()}")

    return pd.read_json(requests.get(feeds[feed_name]).text)


def get_feed_pretty(url: str) -> dict:
    """
    Get the data from a feed and print the time it was last updated.
    :param url: The URL of the feed.
    :return: A dict containing the latest feed data.
    """
    feed_text = json.loads(requests.get(url).text)
    print(f"Last updated at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(feed_text['last_updated']))}")

    return feed_text


def print_feed_data(*feeds: str) -> None:
    """
    Print data about Blue Bikes based on the area you'd like to explore
    :param feeds: The data feeds to explore. Set to 'gbfs' to print a list of available feeds.
    :return: None
    """
    if "gbfs" in feeds:
        print("\nFeeds")
        feeds_text = get_feed_pretty("https://gbfs.bluebikes.com/gbfs/gbfs.json")["data"]["en"]["feeds"]
        feeds_dict = {}

        for feed in feeds_text:
            print(f"{feed['name']}: {feed['url']}")
            feeds_dict[feed["name"]] = feed["url"]

    if "ebikes_at_stations" in feeds:
        print("\nEbikes at Stations")
        text_ebikes = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/ebikes_at_stations.json")
        data_ebikes = text_ebikes["data"]["stations"]

        for station in data_ebikes:
            print(f"\n{station['station_id']}")
            for ebike in station["ebikes"]:
                print(ebike)

    if "system_information" in feeds:
        print("\nSystem Information")
        text_system_info = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/system_information.json")
        data_system_info = text_system_info["data"]

        for key in data_system_info:
            print(f"{key}: {data_system_info[key]}")

    if "station_information" in feeds:
        print("\nStation Information")
        text_station_info = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/station_information.json")
        data_station_info = text_station_info["data"]["stations"]

        for station in data_station_info:
            print(station)

    if "station_status" in feeds:
        print("\nStation Status")
        text_station_status = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/station_status.json")
        data_station_status = text_station_status["data"]["stations"]

        for station in data_station_status:
            print(station)

    if "free_bike_status" in feeds:  # EMPTY
        print("\nFree Bike Status")
        text_free_bike_status = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/free_bike_status.json")
        data_free_bike_status = text_free_bike_status["data"]["bikes"]

        for bike in data_free_bike_status:
            print(bike)

    if "system_hours" in feeds:  # EMPTY
        print("\nSystem Hours")
        text_system_hours = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/system_hours.json")
        data_system_hours = text_system_hours["data"]["rental_hours"]

        for hour in data_system_hours:
            print(hour)

    if "system_calendar" in feeds:
        print("\nSystem Calendar")
        text_system_calendar = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/system_calendar.json")
        data_system_calendar = text_system_calendar["data"]["calendars"]

        for calendar in data_system_calendar:
            print(calendar)

    if "system_regions" in feeds:
        print("System Regions")
        text_system_regions = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/system_regions.json")
        data_system_regions = text_system_regions["data"]["regions"]

        for region in data_system_regions:
            print(region)

    if "system_pricing_plans" in feeds:
        print("\nSystem Pricing Plans")
        text_system_pricing_plans = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/system_pricing_plans.json")
        data_system_pricing_plans = text_system_pricing_plans["data"]["plans"]

        for plan in data_system_pricing_plans:
            print(plan)

    if "system_alerts" in feeds:
        print("\nSystem Alerts")
        text_system_alerts = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/system_alerts.json")
        data_system_alerts = text_system_alerts["data"]["alerts"]

        for alert in data_system_alerts:
            print(alert)

    if "gbfs_versions" in feeds:
        print("\nGBFS Versions")
        text_gbfs_versions = get_feed_pretty("https://gbfs.lyft.com/gbfs/2.3/bos/en/gbfs_versions.json")
        data_gbfs_versions = text_gbfs_versions["data"]["versions"]

        for version in data_gbfs_versions:
            print(version)


if __name__ == "__main__":
    print_feed_data("system_information")
    # print(get_feed_df("station_information"))
