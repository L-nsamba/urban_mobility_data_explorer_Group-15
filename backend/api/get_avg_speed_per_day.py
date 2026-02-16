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
@avg_speed_blueprint.route("/get_avg_speed_per_day/<int:id>", methods=["GET"])
def get_avg_speed_per_day(id):
    #Fetching the average_speed_kmh for a specific trip by its id
    query = text("""
        SELECT trip_id, average_speed_kmh
        FROM trips
        WHERE trip_id = :id
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"id": id}).fetchone()

        if result is None:
            return jsonify({"error": f"No trip found with trip_id {id}"}), 404
        
        return jsonify({
            "trip_id": result.trip_id,  
            "average_speed_kmh": float(result.average_speed_kmh)
        }), 200  #Success returns 200 status code

#Local test case --> swap out the id as needed
if __name__ == "__main__":
    with app.app_context():
        response = get_avg_speed_per_day(5003)
        
        #Properly handles tuple response and print JSON
        if isinstance(response, tuple):
            json_data = response[0].get_json()
            status_code = response[1]
            print(f"Status: {status_code}")
            print(f"Data: {json_data}")
        else:
            print(response.get_json())

#Examples
#GET /get_avg_speed_per_day/1
#GET /get_avg_speed_per_day/42