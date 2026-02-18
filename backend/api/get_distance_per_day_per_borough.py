from flask import Blueprint, jsonify, Flask
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
# Establing connection to db to retrieve the data
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    connect_args={
        "ssl" : {"ca": os.getenv("DB_CA")}
    }
)

# Using blueprint since it is ideal for handling databases with large amounts of data
distance_blueprint = Blueprint("distance", __name__)

# Defining path and HTTP method
@distance_blueprint.route("/get_distance_per_day_per_borough", methods=["GET"])

def get_distance_per_day_per_borough():
    # Accessing the columns from the respective tables
    # In this case, we access the boroughs from the zone table
    # and link them to their respective IDs in the PULocationID column of the trips table
    # Then return the borough's and respective travel days
    query = text("""
        SELECT DATE (t.tpep_pickup_datetime) AS trip_date,
            z.Borough AS borough,
            ROUND(SUM(t.trip_distance), 2) AS total_distance
        FROM trips t
        JOIN zones z ON t.PULocationID =  z.locationid
        GROUP BY trip_date, borough
        ORDER BY trip_date, borough
    """)

    # Returning the date, borough, and total distance 
    # This will help us compare the daily distance covered in each borough per day
    with engine.connect() as conn:
        result = conn.execute(query)
        data = [
            {"date": str(row.trip_date), "borough": row.borough, "total_distance": float(row.total_distance)}
            for row in result
        ]
        return jsonify({"distance_per_day_borough": data})

