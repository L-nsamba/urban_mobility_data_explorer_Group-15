import pandas as pd

def split_transactions(df):
    excluded_logs = []
    
    #Define rules based on parameters above
    # Ensuring datetime columns are parsed properly
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce")

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

    #4. Keeping only 2019 trips
    start_date = pd.Timestamp("2019-01-01")
    end_date = pd.Timestamp("2019-12-31 23:59:59")

    mask_bad = (
        (df["tpep_pickup_datetime"] < start_date) |
        (df["tpep_pickup_datetime"] > end_date)
    )    
    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Outside 2019 date range"
    excluded_logs.append(bad_rows)
    df = df[~mask_bad].copy()

    #5. Trip duration must be greater than 0
    mask_bad = (df["trip_duration_min"] <= 0)
    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Invalid trip_duration_min <= 0"
    excluded_logs.append(bad_rows)
    df = df[~mask_bad].copy()

    #6. Average speed must be positive and greater than 0
    mask_bad = (df["average_speed_kmh"] <= 0)
    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Invalid average_speed_kmh <= 0"
    excluded_logs.append(bad_rows)
    df = df[~mask_bad].copy()

    #7. Trip distance must be > 0
    mask_bad = (df["trip_distance"] <= 0)
    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Invalid trip_distance <= 0"
    excluded_logs.append(bad_rows)
    df = df[~mask_bad].copy()

    #8. Dropoff must be after pickup
    mask_bad = (df["tpep_dropoff_datetime"] <= df["tpep_pickup_datetime"])
    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Dropoff before pickup"
    excluded_logs.append(bad_rows)
    df = df[~mask_bad].copy()

    #9. Unrealistic high speed
    mask_bad = (df["average_speed_kmh"] > 120)
    bad_rows = df[mask_bad].copy()
    bad_rows["exclusion_reason"] = "Unrealistic speed > 120 km/h"
    excluded_logs.append(bad_rows)
    df = df[~mask_bad].copy()

    cleaned_df = df
    excluded_df = pd.concat(excluded_logs, ignore_index=True) if excluded_logs else pd.DataFrame()
    return cleaned_df, excluded_df
