import json
import random
import time

from pymongo import MongoClient
from bson import json_util, ObjectId
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE_NAME = "dash-exam"
CONNECTION_STRING = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

# Create a new thermometer
@app.route("/thermometers", methods=["POST"])
def create_thermometer():
    data = request.get_json()
    thermometer_collection.insert_one(data)
    return jsonify(json.loads(json_util.dumps(data))), 201


# Create new temperature entries for every existing thermometers
@app.route("/thermometers/temperature", methods=["POST"])
def create_temperature_entry_for_every_thermometer():
    data = []
    thermometer_ids = [str(thermometer["_id"]) for thermometer in thermometer_collection.find()]
    for thermometer_id in thermometer_ids:
        data.insert(0, {
            "value": random.randint(20, 30),
            "timestamp": time.ctime(time.time()),
            "thermometer_id": ObjectId(thermometer_id)
        })
    temperature_collection.insert_many(data)
    return jsonify(json.loads(json_util.dumps(data))), 201


if __name__ == "__main__":
    mongo_client = MongoClient(CONNECTION_STRING)
    database = mongo_client.get_database(DATABASE_NAME)
    thermometer_collection = database.get_collection("thermometers")
    temperature_collection = database.get_collection("temperatures")
    app.run(debug=True, port=8000)