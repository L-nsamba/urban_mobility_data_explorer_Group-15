from flask import Blueprint, jsonify, Flask, request
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

#Get Environment variables
load_dotenv()

# Establishing connection to db to retrieve the data
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    connect_args={
        "ssl" : {"ca": os.getenv("DB_CA")}
    }
)

app = Flask(__name__)

#Define Blueprint
trips_hour_blueprint = Blueprint("trips_hour", __name__)

#Define Get Endpoint that returns the total number of trips grouped by the pickup trips_hour
@trips_hour_blueprint.route("/get_trips_per_hour", methods=["GET"])
def get_trips_per_hour():

    #Query parameter to filter trips for that specific date
    date_filter = request.args.get("date")

    if date_filter:
        query = text("""
            SELECT HOUR(tpep_pickup_datetime) AS trip_hour,
                    COUNT(*) AS total_trips
            FROM trips
            WHERE DATE(tpep_pickup_datetime) = :date_filter
            GROUP BY trip_hour
            ORDER BY trip_hour;
        """)
        params = {"date_filter": date_filter}
    else:
        query = text("""
             SELECT HOUR(tpep_pickup_datetime) AS trip_hour,
                     COUNT(*) AS total_trips
             FROM trips
             GROUP BY trip_hour
             ORDER BY trip_hour;
        """)
        params = {}

    try:
        with engine.connect() as conn:
            result = conn.execute(query, params)

            data = [
                {"hour": int(row.trip_hour), "total_trips": int(row.total_trips)}
                for row in result
            ]

        return jsonify({"trips_per_hour": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


