import pandas as pd

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

# Save
print(f"Saving to {OUTPUT_FILE}")
df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df):,} rows")