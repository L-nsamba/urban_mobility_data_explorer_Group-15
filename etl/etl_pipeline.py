import pandas as pd

#Reading and accessing the dataset path
df = pd.read_csv("etl/raw_data/train.csv")

# Dropping rows if missing critical field
df = df.dropna(subset=["pickup_datetime", "dropoff_datetime", "pickup_longitude", "pickup_latitude"])

#Removing outlier (passenger_count < 0 & passenger_count >= 8)
df = df[(df["passenger_count"] > 0) & (df["passenger_count"] <= 8)]

# Creating derived quantity of pickup hour to analyze rush hours
df["pickup_hour"] = pd.to_datetime(df["pickup_datetime"]).dt.hour

#Creating derived quantity of pick up day to analyze weekday vs weekend traffic
df["pickup_dayofweek"] = pd.to_datetime(df["pickup_datetime"]).dt.day_name()

#Saving cleaned dataset
df.to_csv("etl/processed/clean_data.csv", index=False)