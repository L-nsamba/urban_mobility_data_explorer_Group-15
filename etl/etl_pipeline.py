import pandas as pd

#Reading and accessing the dataset path
#df = pd.read_csv("etl/raw_data/train.csv")

# Dropping rows if missing critical field
df = df.dropna(subset=["pickup_datetime", "dropoff_datetime", "pickup_longitude", "pickup_latitude"])

#Removing outlier (passenger_count < 0 & passenger_count >= 8)
df = df[(df["passenger_count"] > 0) & (df["passenger_count"] <= 8)]


#Normalizing timestamp & formatting timestamp, coordinates and numeric fields
# Source and Output Configurations
INPUT_FILE = "urban_mobility_data_explorer_Group-15/etl/raw_data/train.csv" 
OUTPUT_FILE = "urban_mobility_data_explorer_Group-15/etl/clean_data.csv"
DECIMAL_PLACES = 4  # Accuracy only drops to about 11 metres.

#Read CSV
print(f"Reading {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df):,} rows")

#Normalize the timestamps to YYYY-MM-DD HH:MM:SS
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')

#Round the coordinates to 4 decimal places
df['pickup_longitude'] = df['pickup_longitude'].round(DECIMAL_PLACES)
df['pickup_latitude'] = df['pickup_latitude'].round(DECIMAL_PLACES)
df['dropoff_longitude'] = df['dropoff_longitude'].round(DECIMAL_PLACES)
df['dropoff_latitude'] = df['dropoff_latitude'].round(DECIMAL_PLACES)

#Validate longitude range (-180 to 180)
lon_invalid = ((df['pickup_longitude'] < -180) | (df['pickup_longitude'] > 180) | (df['dropoff_longitude'] < -180) | (df['dropoff_longitude'] > 180))
print(f"Invalid longitudes: {lon_invalid.sum()}")

#Validate latitude range (-90 to 90)
lat_invalid = ((df['pickup_latitude'] < -90) | (df['pickup_latitude'] > 90) | (df['dropoff_latitude'] < -90) | (df['dropoff_latitude'] > 90))
print(f"Invalid latitudes: {lat_invalid.sum()}")


#Create and justify atleast additional (1) derived features
#1. My ideas (pickup_days & pickup_hours to analyze rush hour) 
#   free to create others but ensure there's a logical connection
#   between existing elements

# Creating derived quantity of pickup hour to analyze rush hours
df["pickup_hour"] = pd.to_datetime(df["pickup_datetime"]).dt.hour

#Creating derived quantity of pick up day to analyze weekday vs weekend traffic
df["pickup_dayofweek"] = pd.to_datetime(df["pickup_datetime"]).dt.day_name()

#Log for excluded transactions

#Parse datetime
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors="coerce")
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], errors="coerce")

def split_transactions(df):

    excluded_logs = []

    #Define rules based on parameters above
    #1.Missing a critical Fields
    critical = ["pickup_datetime", "dropoff_datetime", "pickup_longitude", "pickup_latitude"]
    mask_bad = (df[critical].isna().any(axis=1)

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

cleaned_df, excluded_df = split_transactions(df)

#Saving cleaned dataset(etl/processed/clean.csv) & excluded logs (etl/excluded_logs/excluded.csv)

cleaned_df.to_csv("etl/processed/clean.csv", index=False)
excluded_df.to_csv("etl/excluded_logs/excluded.csv", index=False)