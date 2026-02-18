<h1 align="center"> 🗺️ URBAN MOBILITY DATA EXPLORER </h1>

### 📋 PROJECT OVERVIEW
This project is an enterprise-level full-stack application built using real-world urban mobility data from the New York City January 2019 Taxi Trip  dataset. The application involves cleaning and processing raw trip data, storing it in a relational database, developing a backend for data queries, and creating a frontend dashboard to explore urban mobility patterns.
<br>

### ⚙️ TECH STACK
### Backend
* <strong>Language : </strong> Python 3.13.12
* <strong>Framework : </strong> Flask 3.1.2
* <strong>ORM : </strong> SQLAlchemy 2.0.46
* <strong> Data Handling : </strong> pandas 3.0.0
* <strong> Database : </strong> MySQL

### Frontend
* <strong>Frontend Stack : </strong> HTML, CSS & JavaScript

### 📂 PROJECT STRUCTURE
```plaintext
├── backend/
|    ├── api/ 
|    ├── app.py
|    └── requirements.txt
├── database/
|    ├── database_setup.py
|    └── urban_mobility_explorer-dump.sql           
├── docs/
|    ├── urban_mobility_data_explorer_erd.pdf
|    ├── urban_mobility_data_explorer_system_architecture.pdf
|    └── api_endpoints.md
├── dsa/
|    ├── frequency.py
|    └── merge_sort.py       
├── etl/
|    ├── raw_data/
|    ├── etl_pipeline.py
|    ├── excluded_logs.py
|    ├── integration.py
|    └── trip_cleaning.py
├── frontend/
|    ├── index.html
|    ├── styles/
|    ├── charts/
|    └── scripts/
├── screenshots/
├── .env.example
├── .gitattributes
├── .gitignore
└──  README.md
```
<br>

### 🛠 PROJECT PLAN & ARCHITECTURE
**Link to System Architecture**: https://drive.google.com/file/d/1LCjnhGtCJYlr8gqgD0ch9cqHbQsDx4fg/view?usp=sharing
<br>
**Link to Database Design Documentation**: https://docs.google.com/document/d/18Bi2BIYgeXfUJe7Cec5Rh4WkCqROOQR2frSWPbLLxp0/edit?usp=sharing
<br>
**Link to Entity Relationship Diagram**: https://drive.google.com/file/d/1Cd5dWxY3CMglkRkfNaBEgtoPrRIrTHlp/view?usp=sharing
<br>

<br>

### 🚀 GETTING STARTED FOR THE PROJECT 
#### 1️⃣ Clone the repo:
 ```
     git clone https://github.com/L-nsamba/urban_mobility_data_explorer_Group-15.git
     cd urban_mobility_data_explorer_Group-15
 ```
#### 2️⃣ Backend Setup
 ```
     cd backend
     pip install -r requirements.txt
 ```
#### 3️⃣ Database Setup
### OPTION A - Quick Setup (Import Pre-Populated Database)
<strong> 1.  Import the dump </strong>
* The repository includes a full SQL dump containing the database schema and cleaned data <br>
⚠️ <strong>Warning: </strong> The SQL dump contains over 2 million rows from the dataset. Ensure you have sufficient RAM storage before importation
* CLI option:
 ```
    mysql -u <username> -p < urban_mobility_explorer-dump.sql
 ```
* Or import using a GUI like MySQL Workbench or DataGrip <br>

<strong> 2. Verify tables are existing </strong>
 ```
    SHOW TABLES;
    trips
    zones
 ```
* The API endpoints can run immediately without executing the ETL pipeline. Re-running the ETL pipeline may cause duplication of data

### OPTION B - Full Setup (Run ETL Pipeline)
<strong> 1. Create an empty database and respective tables </strong>
* Use this option if you want to recreate the database and populate it from scratch <br>
```
    CREATE DATABASE <your_database_name>
    USE <your_database_name>
    CREATE TABLE trips;
    CREATE TABLE zones;    
```
<strong> 2. Configure environment variables </strong>
* Create a ```.env``` file:
 ```
     DB_USER=your_user
     DB_PASS=your_password
     DB_HOST=your_host
     DB_PORT=your_port
     DB_NAME=your_database_name
     DB_CA=path_to_ssl_certificate
 ```
* You can access this information from your MYSQL client of choice e.g Aiven <br>

<strong> 3.  Run the ETL pipeline to populate </strong>
 ```
    python etl/etl_pipeline.py
 ```
* This will the raw taxi trip data, apply exclusion rules, enrich with zone lookup and insert processed records into the database <br>
⚠️ <strong>Warning: </strong> The NYC Yellow Taxi Jan 2019 Dataset contains over 7 millions rows of data. It is advisable to check your RAM storage permissionns with your MYSQL client before running or only entering a significantly smaller number of rows (1-2 million) for test cases. 

#### 4️⃣ Frontend Setup
1. Ensure that ```app.py``` is running.
* This facilitates the connection between the api_endpoints retrieving data from the database and the JavaScript logic in the frontend that creates the visualizations.
```
    python backend/app.py
```
2. Open with Live Server or run ``` http://127.0.0.1:5500/frontend/index.html ``` in your browser

<br>

### 📝 API IMPLEMENTATION

| Endpoint | Method | Description |
|----------- | --------| -------- |  
| /api/get_trips_per_day | GET | Retrieves the daily total number of trips from all yellow taxis from all boroughs |
| /api/get_trips_per_hour | GET | Retrieves total number of trips from each hour of the day from all yellow taxis from all boroughs during the specified time frame/ days | 
| /api/get_fare_per_day_per_borough | GET | Retrieves the daily fare total per borough |
| /api/get_avg_speed_per_day | GET | Retrieves the average speed (in kmh) of all yellow taxis from all boroughs from each day |
| /api/get_distance_per_day_per_borough | GET | Retrieves the total distance (in miles) of all yellow taxis from all boroughs from each day |

#### 📌 NOTE
* The MySQL dump dataset contains approximately 2.5 million records out of the 7.4 million, covering the period from January 1st, 2019 to January 12th, 2019
* For more information about the api endpoint documentation: <br>
 ```cd docs/api_endpoints.md```





