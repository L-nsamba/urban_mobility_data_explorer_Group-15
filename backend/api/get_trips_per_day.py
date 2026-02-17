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

# Creating flask app
app = Flask(__name__)

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
    
# Local test case to ensure it retrieves the fare data
if __name__ == "__main__":
    with app.app_context():
        response = get_trips_per_day()
        print(response.get_json())

