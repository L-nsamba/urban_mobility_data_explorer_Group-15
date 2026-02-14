from trip_cleaning import clean_data
from excluded_logs import split_transactions
from integration import integrate_data
from sqlalchemy import create_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
# Cleaning data
df = clean_data("etl/raw_data/yellow_tripdata_2019-01.parquet")

# Separating the clean from the erroneous data
cleaned_df, excluded_df = split_transactions(df)

# Integrating with lookup + zones

integrated_df, zones = integrate_data(
    "etl/raw_data/yellow_tripdata_2019-01.parquet",
    "etl/raw_data/taxi_zone_lookup.csv",
    "etl/raw_data/taxi_zones/taxi_zones.shp"
)

# Creation of database connection
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    connect_args={
        "ssl" : {"ca": os.getenv("DB_CA")}
    }
)

# Injecting the zones csv data into the zones table
zones_df = pd.read_csv("etl/raw_data/taxi_zone_lookup.csv")

# Error handling to ensure correct id initial reference upon data entry
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT (*) FROM zones")).scalar()

if count == 0:
    zones_df.to_sql("zones", engine, if_exists="append", index=False, chunksize=10000)
    
# Defining of the exact columns to enter into the Trip table before being passed into the db
trip_columns = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount",
    "PULocationID",
    "DOLocationID",
    "trip_duration_min",
    "fare_per_km",
    "average_speed_kmh"
]

# Filtering out only the columns we want to be displayed
trips_df = cleaned_df[trip_columns]

# Injecting the cleaned data into the database
trips_df.to_sql("trips", engine, if_exists="append", index=False, chunksize=10000)
print("Data successfully injected into database!")