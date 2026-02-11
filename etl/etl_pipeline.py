import pandas as pd

#Reading and accessing the dataset path
df = pd.read_csv("etl/raw_data/train.csv")

# Dropping rows if missing critical field
df = df.dropna(subset=["pickup_datetime", "dropoff_datetime", "pickup_longitude", "pickup_latitude"])

#Removing outlier (passenger_count < 0 & passenger_count >= 8)
df = df[(df["passenger_count"] > 0) & (df["passenger_count"] <= 8)]


#Normalizing timestamp & formatting timestamp, coordinates and numeric fields
#Co-ordinate Configurations
DECIMAL_PLACES = 4  # Accuracy only drops to about 11 metres.

#Read CSV
#print(f"Reading INPUT_FILE...")
#df = pd.read_csv("etl/raw_data/train.csv")
#print(f"Loaded {len(df):,} rows")

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

#Log for excluded transactionns

#Saving cleaned dataset(etl/processed/clean.csv) & excluded data (etl/excluded_logs/excluded.csv)
