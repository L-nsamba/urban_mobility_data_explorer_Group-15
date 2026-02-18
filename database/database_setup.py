from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
# 1. Database connection
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    connect_args={
        "ssl" : {"ca": os.getenv("DB_CA")}
    }
)

Base = declarative_base()

#2. Defining tables
class Zone(Base):
    __tablename__ = "zones"

    locationid = Column(Integer, primary_key=True)
    Borough = Column(String(100))
    Zone = Column(String(255))
    service_zone = Column(String(100))

# 3. Create table

class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    tpep_pickup_datetime = Column(DateTime)
    tpep_dropoff_datetime = Column(DateTime)
    passenger_count = Column(Integer)
    trip_distance = Column(Float)
    fare_amount = Column(Float)
    tip_amount = Column(Float)
    total_amount = Column(Float)
    
    # Foreign keys 
    PULocationID = Column(Integer,  ForeignKey("zones.locationid"))
    DOLocationID = Column(Integer,  ForeignKey("zones.locationid"))

    trip_duration_min = Column(Float)
    fare_per_km = Column(Float)
    average_speed_kmh = Column(Float)

Base.metadata.create_all(engine)

print("Database connected and table created")