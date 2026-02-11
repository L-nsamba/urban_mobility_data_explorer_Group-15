from trip_cleaning import clean_data
from excluded_logs import split_transactions
from integration import integrate_data

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

cleaned_df.to_csv("etl/processed_data/clean.csv", index=False)
excluded_df.to_csv("etl/processed_data/excluded.csv", index=False)
integrated_df.to_csv("etl/processed_data/integrated.csv", index=False)