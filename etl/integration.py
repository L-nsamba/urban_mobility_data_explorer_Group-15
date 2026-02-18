import pandas as pd
import geopandas as gdp

# This function links the IDs in the yellow_tripdata.parquet file to the corresponding location in the taxi lookup file
def integrate_data(trips_path, lookup_path, zones_path):
    
    # Loading the taxi trip data
    if trips_path.endswith(".parquet"):
        trips = pd.read_parquet(trips_path)
    else:
        trips = pd.read_csv(trips_path)

    # Loading taxi lookup zone data
    lookup = pd.read_csv(lookup_path)

    # Joining taxi trips data with lookup for pickup & dropoff
    # Connecting the numeric IDs for PULocationID & DOLocationID to the corresponding actual location in the taxi_zone_lookup
    trips = trips.merge(lookup, left_on="PULocationID", right_on="LocationID", how="left")
    trips = trips.merge(lookup, left_on="DOLocationID", right_on="LocationID", how="left",
                        suffixes=("_pickup", "_dropoff"))
    
    # Loading metadata 
    zones = gdp.read_file(zones_path)

    return trips, zones