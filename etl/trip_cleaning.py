import pandas as pd

def clean_data(path):

    # Handling both .parquet and .csv formats
    if path.endswith(".parquet"):
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path)

    #Reading and accessing the dataset path
    df = pd.read_parquet(path)

    # Dropping rows if missing critical field
    df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance"])

    #Removing outlier (passenger_count < 0 & passenger_count >= 8)
    df = df[(df["passenger_count"] > 0) & (df["passenger_count"] <= 8)]

    #Normalize the timestamps to YYYY-MM-DD HH:MM:SS
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.strftime('%Y-%m-%d %H:%M:%S')
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"]).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Creating derived quantity of pickup hour to analyze rush hours
    df["pickup_hour"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.hour

    #Creating derived quantity of pick up day to analyze weekday vs weekend traffic
    df["pickup_dayofweek"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.day_name()

    return df
