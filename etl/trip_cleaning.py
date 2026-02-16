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

    #Creating derived quantity of pickup day to analyze weekday vs weekend traffic
    df["pickup_dayofweek"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.day_name()

    # Creating derived quantity of trip duration (minutes)
    # Also remvoing the outlier if the trip is negative or zero which is invalid
    df["trip_duration_min"] = ((pd.to_datetime(df["tpep_dropoff_datetime"])
                               - pd.to_datetime(df["tpep_pickup_datetime"])).dt.total_seconds() / 60).round(2)
    df = df[df["trip_duration_min"] > 0]

    # Creating derived quantity of fare per km to analyse the cost efficiency
    # It is going to be fare_amount/trip distance
    # To avoid division by zero
    df = df[df["trip_distance"] > 0]
    df["fare_per_km"] = (df["fare_amount"] / df["trip_distance"]).round(2)

    # Removing outlier of unrealistic fare per km values
    df = df[(df["fare_per_km"] >= 0) & (df["fare_per_km"] <= 100)]

    # Creating derived quantity of average speed (km/h) to analyse congestion patterns
    # It is calculated as (trip distance/ trip duration) / 60
    df["average_speed_kmh"] = ((df["trip_distance"] / df["trip_duration_min"]) * 60).round(2)

    # Removing outlier of unrealistic speed
    df = df[(df["average_speed_kmh"] >= 0) & (df["fare_per_km"] <= 150)]

    return df

