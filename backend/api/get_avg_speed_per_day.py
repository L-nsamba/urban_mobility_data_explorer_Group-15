from flask import Blueprint, jsonify, Flask
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

#Establishing connection to db to retrieve the data
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    connect_args={
        "ssl": {"ca": os.getenv("DB_CA")}
    }
)

app = Flask(__name__)

avg_speed_blueprint = Blueprint("avg_speed", __name__)

#id is passed directly in the URL e.g. /get_avg_speed_per_day/42
@avg_speed_blueprint.route("/get_avg_speed_per_day", methods=["GET"])
def get_avg_speed_per_day():
    #Fetching the average_speed_kmh for a specific trip by its id
    query = text("""
        SELECT DATE(tpep_pickup_datetime) AS trip_date,
            ROUND(AVG(average_speed_kmh), 2) AS avg_speed_kmh
        FROM trips
        GROUP BY trip_date
        ORDER BY trip_date;
""")

    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            data =  [
                {
                    "date": str(row.trip_date),
                    "avg_speed_kmh":  float(row.avg_speed_kmh)
                }
                for row in result
            ]
        return jsonify({"avg_speed_per_day": data})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Local test case --> swap out the id as needed
if __name__ == "__main__":
    with app.app_context():
        response = get_avg_speed_per_day()
        print(response.get_json())