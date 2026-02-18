from flask import Flask, jsonify, Blueprint
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection engine
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

trips_day_blueprint = Blueprint("trips_day", __name__)

#Defining the endpoint
@trips_day_blueprint.route('/get_trips_per_day', methods=['GET'])
def get_trips_per_day():

    query = text("""
        SELECT DATE(tpep_pickup_datetime) AS trip_date, 
                COUNT(*) AS total_trips
        FROM trips
        GROUP BY trip_date
        ORDER BY trip_date;
    """)

    try:
        
        with engine.connect() as conn:
            result = conn.execute(query)
            data = [
                {
                    "date": str(row.trip_date),
                    "total_trips": row.total_trips
                }
                for row in result
            ]

        return jsonify({"trips_per_day": data})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

