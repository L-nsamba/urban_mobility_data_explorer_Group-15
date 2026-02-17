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
|    └── rank.py       
├── etl/
|    ├── raw_data/
|    ├── etl_pipeline.py
|    ├── excluded_logs.py
|    ├── integration.py
|    └── trip_cleaning.py
├── frontend/
|    ├── index.html
|    ├── styles/
|    └── scripts/
├── .env
├── .gitattributes
├── .gitignore
└──  README.md
```

### 🛠 PROJECT PLAN & ARCHITECTURE
**Link to System Architecture**: https://drive.google.com/file/d/1LCjnhGtCJYlr8gqgD0ch9cqHbQsDx4fg/view?usp=sharing
<br>
**Link to Database Design Documentation**: https://docs.google.com/document/d/18Bi2BIYgeXfUJe7Cec5Rh4WkCqROOQR2frSWPbLLxp0/edit?usp=sharing
<br>

### 🚀 GETTING STARTED FOR THE PROJECT (IN-PROGRESS)
#### 1. Clone the repo:
 ```
     git clone https://github.com/L-nsamba/urban_mobility_data_explorer_Group-15.git
     cd urban_mobility_data_explorer_Group-15
 ```
#### 2. Backend setup
 ```
     cd backend
     pip install -r requirements.txt
 ```
#### 3. Database Setup
### OPTION A - Quick Setup (Import Pre-Populated Database)
* 1️⃣ <strong> Import the dump </strong>
* The repository includes a full SQL dump containing the database schema and cleaned data
* CLI option:
 ```
    mysql -u <username> -p < urban_mobility_explorer-dump.sql
 ```
* Or import using a GUI like MySQL Workbench or DataGrip
* 2️⃣ <strong> Verify tables are existing </strong>
 ```
    SHOW TABLES;
    trips
    zones
 ```
* The API endpoints can run immediately without executing the ETL pipeline. Re-running the ETL pipeline may cause duplication of data

### OPTION B - Full Setup (Run ETL Pipeline)
* Use this option if you want to recreate the database and populate it from scratch
* 1️⃣ <strong> Create an empty database and respective tables </strong>
```
    CREATE DATABASE <your_database_name>
    USE <your_database_name>
    CREATE TABLE trips;
    CREATE TABLE zones;    
```
* 2️⃣ <strong> Configure environment variables </strong>
* Create a ```.env``` file:
 ```
     DB_USER=your_user
     DB_PASS=your_password
     DB_HOST=your_host
     DB_PORT=your_port
     DB_NAME=your_database_name
     DB_CA=path_to_ssl_certificate
 ```
* You can access this information from your MYSQL client of choice e.g Aiven
* 3️⃣ <strong> Run the ETL pipeline to populate </strong>
 ```
    python etl/etl_pipeline.py
 ```
* This will the raw taxi trip data, apply exclusion rules, enrich with zone lookup and insert processed records into the datbase
* ⚠️ <strong>Warning </strong>
* The NYC Yellow Taxi Jan 2019 Dataset contains over 7 millions rows of data. It is advisable to check your RAM storage permissionns with your MYSQL client before running or only entering a significantly smaller number of rows (1-2 million) for test cases. 


