import pandas as pd

#Define rules based on parameters above

def split_transactions(df):
    excluded_logs = []

    # Ensuring datetime columns are parsed properly
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce")

    #Helper function to take bad rows, add a reason, append and remove them
    def apply_rule(df, mask_bad, reason):
        if mask_bad.any():
            bad_rows = df[mask_bad].copy()
            bad_rows["exclusion_reason"] = reason
            excluded_logs.append(bad_rows)
        return df.loc[~mask_bad].copy()

    #1.Missing a critical Fields
    critical = ["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance"]
    df = apply_rule(df, df[critical].isna().any(axis=1), "Missing critical fields")

    #2.Passenger Count must be >0 and <= 8)
    df = apply_rule(df, (df["passenger_count"] <= 0) | (df["passenger_count"] > 8), "Invalid passenger_count")

    #3. Amounts must be positive and greater than 0
    df = apply_rule(
        df,
        (df["fare_amount"] <= 0) | (df["total_amount"] <= 0),
        "Amount must be positive and greater than 0"
    )

    #4. Keeping only 2019 trips
    start_date = pd.Timestamp("2019-01-01")
    end_date = pd.Timestamp("2019-01-31 23:59:59")
    df = apply_rule(
        df,
        (df["tpep_pickup_datetime"] < start_date) | (df["tpep_pickup_datetime"] > end_date),
        "Outside Jan 2019 date range"
    )

    #5. Trip duration must be greater than 0
    df = apply_rule(df, df["trip_duration_min"] <= 0, "Invalid trip_duration_min <= 0")

    #6. Average speed must be positive and greater than 0
    df = apply_rule(df, df["average_speed_kmh"] <= 0, "Invalid average_speed_kmh <= 0")

    #7. Trip distance must be > 0
    df = apply_rule(df, df["trip_distance"] <= 0, "Invalid trip_distance <= 0")

    #8. Dropoff must be after pickup
    df = apply_rule(
        df,
        df["tpep_dropoff_datetime"] <= df["tpep_pickup_datetime"],
        "Dropoff before pickup"
    )

    #9. Unrealistic high speed
    df = apply_rule(df, df["average_speed_kmh"] > 120, "Unrealistic speed > 120 km/h")

    cleaned_df = df
    excluded_df = pd.concat(excluded_logs, ignore_index=True) if excluded_logs else pd.DataFrame()

    return cleaned_df, excluded_df
