from flask import Flask
from api.get_trips_per_day import trips_day_blueprint
from api.get_trips_per_hour import trips_hour_blueprint
from api.get_distance_per_day_per_borough import distance_blueprint
from api.get_fare_per_day_per_borough import fare_blueprint
from api.get_avg_speed_per_day import avg_speed_blueprint

def create_app():
    app = Flask(__name__)

    # Registering blueprints with a common prefix of "/api"
    app.register_blueprint(trips_day_blueprint, url_prefix="/api")
    app.register_blueprint(trips_hour_blueprint, url_prefix="/api")
    app.register_blueprint(distance_blueprint, url_prefix="/api")
    app.register_blueprint(fare_blueprint, url_prefix="/api")
    app.register_blueprint(avg_speed_blueprint, url_prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)