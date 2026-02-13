from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import pandas as pd

# 1. Database connection

DB_USER = ""
DB_PASSWORD = ""
DB_NAME = ""

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}")
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
    tpep_pickup_datetime = Column(String(50))
    tpep_dropoff_datetime = Column(String(50))
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
    average_speed_km_h = Column(Float)

Base.metadata.create_all(engine)

print("Database connected and table created")

# 3. Read clean csv

df = pd.read_csv("clean.csv")

# 4. Insert data

Session = sessionmaker(bind=engine)
session = Session()

for index, row in df.iterrows():
    trip = Trip(
        tpep_pickup_datetime=row["tpep_pickup_datetime"],
        tpep_dropoff_datetime=row["tpep_dropoff_datetime"],
        passenger_count=row["passenger_count"],
        trip_distance=row["trip_distance"],
        fare_amount=row["fare_amount"],
        tip_amount=row["tip_amount"],
        total_amount=row["total_amount"],
        PULocationID=row["PULocationID"],
        DOLocationID=row["DOLocationID"],
        trip_duration_min=row["trip_duration_min"],
        fare_per_km=row["fare_per_km"],
        average_speed_km_h=row["average_speed_km_h"]
    )

    session.add(trip)

session.commit()
session.close()

print("Data inserted successfully!")
