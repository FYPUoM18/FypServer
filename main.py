from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

# Define your MongoDB connection settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'fyp_data'
MONGO_COLLECTION = 'sensordata'

# Create a MongoDB client and connect to the database
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Define the data model using Pydantic
class SensorData(BaseModel):
    timestamp: int
    gyro_x: float
    gyro_y: float
    gyro_z: float
    gamerv_x: float
    gamerv_y: float
    gamerv_z: float
    gamerv_w: float
    acce_x: float
    acce_y: float
    acce_z: float
    deviceId: str
    building: str

@app.post("/sensor-data")
async def receive_sensor_data(sensor_data_list: list[SensorData]):
    # Convert the list of Pydantic models to a list of dictionaries
    print("Recieved new data")
    data_list = [item.dict() for item in sensor_data_list]

    # Insert the data into MongoDB
    result = collection.insert_many(data_list)

    return {"message": "Data received and stored successfully."}

@app.get("/sensor-data")
def get_sensor_data():
    # Retrieve sensor data from MongoDB or any other data source
    # Perform any necessary processing or filtering
    # Return the sensor data as a response
    print("GET request received")
    return {"message": "GET request received"}

@app.post("/api/data")
def get_data(start_time: str, end_time: str, building_name: str, device_id: str):
    # Convert start_time and end_time to datetime objects
    start_datetime = datetime.fromisoformat(start_time)
    end_datetime = datetime.fromisoformat(end_time)

    # Query MongoDB based on the provided parameters
    query = {
        'timestamp': {'$gte': start_datetime, '$lte': end_datetime},
        'building': building_name,
        'device_id': device_id
    }
    result = list(collection.find(query))

    return result

@app.post("/upload_files")
async def upload_files(files: list[UploadFile] = File(...)):
    for file in files:
        file_path = f"C:\\Users\\musab\\OneDrive\\Desktop\\projects\\test\\{file.filename}"
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
    
    return {"message": "Files uploaded successfully"}

@app.get("/api/buildings")
def get_building_names():
    # Use distinct() method to retrieve unique building names
    building_names = collection.distinct('building')

    return building_names