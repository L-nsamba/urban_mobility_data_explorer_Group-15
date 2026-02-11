import pandas as pd

def split_transactions(df):
    excluded_logs = []
    
    #Define rules based on parameters above
    #1.Missing a critical Fields
    critical = ["pickup_datetime", "dropoff_datetime", "pickup_longitude", "pickup_latitude"]
    mask_bad = (df[critical].isna().any(axis=1))

    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Missing Critical fields"
    excluded_logs.append(bad_rows)

    df = df[~mask_bad].copy()

    #2.Passenger Count must be >0 and <= 8)
    mask_bad = (df["passenger_count"] <= 0) | (df["passenger_count"] > 8)

    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Invalid passenger_count"
    excluded_logs.append(bad_rows)

    df = df[~mask_bad].copy()

    #3.Longitude range must be between -180 and 180
    mask_bad = (
        (df["pickup_longitude"] < -180) | (df["pickup_longitude"] > 180) |
        (df["dropoff_longitude"] < -180) | (df["dropoff_longitude"] > 180)
    )

    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Invalid longitude_range"
    excluded_logs.append(bad_rows)

    df = df[~mask_bad].copy()

    #4.Latitude range must be between -90 and 90
    mask_bad = (
        (df["pickup_latitude"] < -90) | (df["pickup_latitude"] > 90) |
        (df["dropoff_latitude"] < -90) | (df["dropoff_latitude"] > 90)
    )

    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Invalid latitude_range"
    excluded_logs.append(bad_rows)

    df = df[~mask_bad].copy()

    #5.Possible Minimum trip_duration
    mask_bad = (df["trip_duration"] < 120)

    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Trip Duration is too short"
    excluded_logs.append(bad_rows)
    df = df[~mask_bad].copy()

    cleaned_df = df
    excluded_df = pd.concat(excluded_logs, ignore_index=True) if excluded_logs else pd.DataFrame()
    return cleaned_df, excluded_df
