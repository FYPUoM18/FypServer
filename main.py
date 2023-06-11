from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

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