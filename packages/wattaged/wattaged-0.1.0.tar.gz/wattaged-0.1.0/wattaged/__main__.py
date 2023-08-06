#!/usr/bin/env python3
"""Module doc"""

import sys
import argparse
import os

import pandas as pd  # type: ignore
from dateutil import parser as dateparser


def listdir_abs(path):
    return list(map(lambda f: os.path.join(path, f), os.listdir(path)))


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Computes how much watt-hours were consummed in the time span requested"
    )
    parser.add_argument(
        "--start",
        default="",
        help="The start date to compute the consumption, any format recognised by dateutil.parser.parse will work. By default, starts at the last boot time.",
    )
    parser.add_argument(
        "--end",
        default="",
        help="The end date to compute the consumption. By default computes till the latest record.",
    )
    parser.add_argument(
        "--logdir",
        default="/var/log/wattaged",
        help="The path where .log and .log.gz-ddMMYY are stored",
    )
    args = parser.parse_args()
    dfs = []

    for f in listdir_abs(args.logdir):
        if f.endswith(".gz"):
            dfs.append(
                pd.read_csv(
                    f,
                    compression="gzip",
                    header=0,
                    sep="\t",
                    names=["date", "watts"],
                )
            )
        elif f.endswith(".log"):
            dfs.append(
                pd.read_csv(
                    f,
                    header=0,
                    sep="\t",
                    names=["date", "watts"],
                )
            )
    df = pd.concat(dfs)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date")

    mean_resolution = df["date"].diff(1).mean()

    if len(args.start) > 0:
        start = (
            pd.to_datetime(dateparser.parse(args.start), utc=True) - mean_resolution / 2
        )
    else:
        start_boot = (
            pd.to_datetime(dateparser.parse(get_last_boot_date()), utc=True)
            - mean_resolution / 2
        )
        start_first = df.iloc[0]["date"]
        start = max(start_first, start_boot)

    if len(args.end) > 0:
        end = pd.to_datetime(dateparser.parse(args.end), utc=True) + mean_resolution / 2
    else:
        end = df.iloc[-1]["date"]
    df = df[df["date"].between(start, end)]

    total_watt_hours = 0

    for i in range(len(df) - 1):
        wh = integral_linear_interp(
            x1=pd_timestamp_to_hours(df.iloc[i]["date"]),
            y1=df.iloc[i]["watts"],
            x2=pd_timestamp_to_hours(df.iloc[i + 1]["date"]),
            y2=df.iloc[i + 1]["watts"],
        )
        total_watt_hours += wh
    # Paris 2021-07-27 kWh price is 0.14 EUR
    print(f"{total_watt_hours:.3f}\tWh between {start} and {end}")
    print(f'\033[94m~={total_watt_hours*0.14/1000:.3f} EUR\033[0m', file=sys.stderr)


def pd_timestamp_to_hours(ts) -> float:
    return float(ts.value * 1e-9 / 3600)


def get_last_boot_date() -> pd.Timestamp:
    return os.popen("/usr/bin/who -b").read()[-17:-1]


def integral_linear_interp(x1, y1, x2, y2):
    # Computes the integral of the linear interpolation between (x1, y1) and (x2, y2)
    # (x2-x1) is time
    # (y2-y1) is watts
    # the area under the curve is watts*time = energy (Wh)
    # linear interp formula:
    # (y2-y1)/(x2-x1) * (x-x1) + y1
    # the formula below is that thing, but integrated for x between x1 and x2

    return -0.5 * (x1 - x2) * (y1 + y2)


if __name__ == "__main__":
    main()
