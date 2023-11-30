import requests
import json
import pandas as pd
import time

from mbuskey import API_KEY

ENDPOINT = "https://mbus.ltp.umich.edu/bustime/api/v3"


def get_oxford_buses():
    """Get all active vehicles"""
    params = {"key": API_KEY, "format": "json", "rt": "OS"}
    response = requests.get(f"{ENDPOINT}/getvehicles", params=params)
    if response.json()["bustime-response"].get("error"):
        return []
    return [bus for bus in response.json()["bustime-response"].get("vehicle")]


while True:
    # get oxford shuttle buses
    buses = get_oxford_buses()

    try:
        df = pd.read_csv("oxford_buses.csv")
    except:
        df = pd.DataFrame()

    # Breaks the loop if no buses have been returned in 10 tries
    empty = 0
    if not buses:
        empty + 1

    if empty > 10:
        print("No buses found")
        break

    # If there are buses, append them to the csv
    if buses:
        if df.empty:
            df = pd.DataFrame(buses)
        else:
            df = pd.concat([df, pd.DataFrame(buses)])

    # drop duplicates
    df.drop_duplicates(
        subset=[
            "vid",
            "hdg",
            "pid",
            "rt",
            "des",
            "pdist",
            "dly",
            "spd",
            "tatripid",
            "origtatripno",
            "tablockid",
            "zone",
            "mode",
            "psgld",
            "stst",
            "stsd",
        ],
        inplace=True,
    )

    print(df.shape)

    # Save the csv
    df.to_csv("oxford_buses.csv", index=False)

    # Wait 10 mins to loop
    time.sleep(600)

print("broken")
