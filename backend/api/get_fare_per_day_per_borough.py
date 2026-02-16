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

app = Flask(__name__)

# Using blueprint, it is the ideal for databases with large amounts of data
fare_blueprint = Blueprint("fare", __name__)

# Definning the path and HTTP Method which is Get
@fare_blueprint.route("/get_fare_per_day_per_borough", methods=["GET"])

def get_fare_per_day_per_borough():
    # We first access the attributes from the respective tables, trips and zones
    # We access the boroughs from the zone table
    # and link them to their respective IDs in the PULocationID field
    # then return the bourough's total fare and respective travel days
    # Returnin the date, borough and total fare
    query = text("""
        SELECT DATE(t.tpep_pickup_datetime) AS trip_date,
            z.Borough AS borough,
        ROUND(SUM(t.total_amount), 2) AS total_fare
        FROM trips t
        JOIN zones z ON t.PULocationID = z.locationid
        GROUP BY trip_date, borough
        ORDER BY trip_date, borough
    """)

    # Get_fare_per_day_per_borough will help in comparing the fare for trips daily in each borough
    with engine.connect() as conn:
        result = conn.execute(query)
        data = [
            {
                "date": str(row.trip_date),
                "borough": row.borough,
                "total_fare": float(row.total_fare)
            }
            for row in result
        ]
        return jsonify({"fare_per_day_per_borough": data})

# Local test case to ensure it retrieves the fare data
if __name__ == "__main__":
    with app.app_context():
        response = get_fare_per_day_per_borough()
        print(response.get_json())
