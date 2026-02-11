import pandas as pd

#Reading and accessing the dataset path
df = pd.read_csv("etl/raw_data/train.csv")

# Dropping rows if missing critical field
df = df.dropna(subset=["pickup_datetime", "dropoff_datetime", "pickup_longitude", "pickup_latitude"])

#Removing outlier (passenger_count < 0 & passenger_count >= 8)
df = df[(df["passenger_count"] > 0) & (df["passenger_count"] <= 8)]


#Normalizing timestamp & formatting timestamp, coordinates and numeric fields
#1. Decimal points for longitude & latitude reduce from 6 dp to maybe 3 or 4
#2. Ensure all time is in standard format (YYY-MM-DD HH:MM:SS)
#3. Ensure range of longitudes is between -180 and 180
#4. Ensure range of latitudes is between -90 and 90


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