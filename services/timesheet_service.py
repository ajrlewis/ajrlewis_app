from loguru import logger
import pandas as pd

daily_rate = 420069  # daily rate in satoshis


def main():
    df = pd.read_csv("backups/timesheet.csv")

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    df["year"] = df["date"].apply(lambda d: d.year)
    df["month"] = df["date"].apply(lambda d: d.month)
    df["description"] = df["date"].astype(str) + ": " + df["description"]
    print(df)

    gb = df.groupby(["client_name", "year", "month"])
    df = gb.agg(description=("description", list), duration=("date", len))
    df["cost"] = df["duration"] * daily_rate

    print()
    print(df)


if __name__ == "__main__":
    main()
