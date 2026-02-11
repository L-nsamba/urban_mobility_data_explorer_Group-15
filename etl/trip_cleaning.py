import pandas as pd

def clean_data(path):
    #Reading and accessing the dataset path
    df = pd.read_csv(path)

    # Dropping rows if missing critical field
    df = df.dropna(subset=["pickup_datetime", "dropoff_datetime", "pickup_longitude", "pickup_latitude"])

    #Removing outlier (passenger_count < 0 & passenger_count >= 8)
    df = df[(df["passenger_count"] > 0) & (df["passenger_count"] <= 8)]

    #Co-ordinate Configurations
    DECIMAL_PLACES = 4  # Accuracy only drops to about 11 metres.

    #Normalize the timestamps to YYYY-MM-DD HH:MM:SS
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')

    #Round the coordinates to 4 decimal places
    df['pickup_longitude'] = df['pickup_longitude'].round(DECIMAL_PLACES)
    df['pickup_latitude'] = df['pickup_latitude'].round(DECIMAL_PLACES)
    df['dropoff_longitude'] = df['dropoff_longitude'].round(DECIMAL_PLACES)
    df['dropoff_latitude'] = df['dropoff_latitude'].round(DECIMAL_PLACES)


    # Creating derived quantity of pickup hour to analyze rush hours
    df["pickup_hour"] = pd.to_datetime(df["pickup_datetime"]).dt.hour

    #Creating derived quantity of pick up day to analyze weekday vs weekend traffic
    df["pickup_dayofweek"] = pd.to_datetime(df["pickup_datetime"]).dt.day_name()

    return df
