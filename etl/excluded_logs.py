import pandas as pd

def split_transactions(df):
    excluded_logs = []
    
    #Define rules based on parameters above
    #1.Missing a critical Fields
    critical = ["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance"]
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

    #3. Amounts must be positive and greater than 0
    mask_bad = ((df["fare_amount"] <= 0) |
                (df["total_amount"] <= 0))
    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Amount must be positive and greater than 0"
    excluded_logs.append(bad_rows)
    df = df[~mask_bad].copy()

    cleaned_df = df
    excluded_df = pd.concat(excluded_logs, ignore_index=True) if excluded_logs else pd.DataFrame()
    return cleaned_df, excluded_df
