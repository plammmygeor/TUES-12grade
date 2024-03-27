import json
from flask import Flask, request, jsonify

from time import time
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient

from database import get_database

app = Flask(__name__)

# Да се създаде нов сензор в колекцията за сензори на вашата база от данни.
# Заявката приема JSON тяло с информация за сензора.
# Заявката връща новосъздадения сензор.
@app.route("/sensors", methods=["POST"])
def create_air_quality_sensor():
    air_data = request.get_json()
    air_sensor = {
        "city": air_data.get("city"),
        "type": air_data.get("type")
    }
    air_quality_sensor_collection.insert_one(air_sensor)
    return jsonify(json.loads(json_util.dumps(air_sensor))), 201


# Да се промени информацията за даден сензор.
# Заявката приема JSON тяло с нова информация за сензора.
# Заявката връща променения сензор.
@app.route("/sensors/<sensor_id>", methods=["PUT"])
def update_air_quality_sensor(sensor_id):
    air_sensor = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if air_sensor:
        air_data = request.get_json()
        air_sensor = {
        	"city": air_data.get("city"),
        	"type": air_data.get("type")
    	}
        air_quality_sensor_collection.update_one({"_id": ObjectId(sensor_id)}, {"$set": air_sensor})
        return jsonify(json.loads(json_util.dumps(air_sensor))), 200
    else:
        return jsonify({"error": "Air sensor not found"}), 404

# Да се изтрие информацията за даден сензор.
# Заявката не приема тяло.
# Заявката връща информация дали изтриването е било успешно.
@app.route("/sensors/<sensor_id>", methods=["DELETE"])
def delete_sensor(sensor_id):
    air_sensor = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if air_sensor:
        air_quality_sensor_collection.delete_one({"_id": ObjectId(sensor_id)})
        return "", 204
    else:
        return jsonify({"error": "Sensor not found"}), 404

# Да се добави информация за получени данни от съответен сензор.
# Заявката приема JSON тяло.
# Заявката връща новосъздадения запис.
@app.route("/sensors/<sensor_id>/data", methods=["POST"])
def create_air_quality_sensor_data_entry(sensor_id):
    air_sensor_data = {
        "sensor_id": sensor_id,
        "timestamp": time()
    }
    air_quality_sensor_data_collection.insert_one(air_sensor_data)
    return jsonify(json.loads(json_util.dumps(air_sensor_data))), 201


# Да се изтрие записана информация за получени данни.
# Заявката не приема тяло.
# Заявката връща информация дали изтриването е било успешно
@app.route("/sensors/<sensor_id>/data/<data_id>", methods=["DELETE"])
def delete_air_quality_sensor_data_entry(sensor_id, data_id):
    air_sensor_data = air_quality_sensor_data_collection.find_one({"sensor_id": ObjectId(sensor_id), "_id": ObjectId(data_id)})
    if air_sensor_data:
        air_quality_sensor_data_collection.delete_one({"_id": ObjectId(data_id)})
        return "", 204
    else:
        return jsonify({"error": "Sensor data not found"}), 404

# Да се изтрие записана информация за получени данни.
# Заявката не приема тяло.
# Заявката връща информация дали изтриването е било успешно
@app.route("/sensors/<sensor_id>", methods=["GET"])
def get_air_quality_sensor_by_id(sensor_id):
    air_sensor = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if air_sensor:
        return jsonify({"Info": json_util.dumps(air_sensor)}), 200
    else:
        return jsonify({"error": "Sensor not found"}), 404

# Да се върнат всички сензори от даден тип сортирани по град в низходящ ред.
# Заявката не приема тяло.
# Заявката връща списък с правилно подредени сензори.
@app.route("/sensors/<type>", methods=["GET"])
def get_air_quality_sensor_by_type_sorted_by_city_descending(sensor_id):
    sort_air_sensor = air_quality_sensor_collection.find({"type": type}).sort("city", -1)
    sorted_sensor_list = list(sort_air_sensor)
    return jsonify({"Air sensor sorted data": sorted_sensor_list}), 200

# Да се върне средно аритметично на всички стойности, отчетени от даден сензор.
# Заявката не приема тяло.
# Заявката връща средноаритметичната стойност за дадения сензор.
@app.route("/sensors/<sensor_id>/average", methods=["GET"])
def get_average_air_quality_by_sensor(sensor_id):
    air_sensor = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if air_sensor:
        read = air_sensor.get("read", []) 
        if read:
            average_value = sum(read) / len(read)
            return jsonify({"Average_value": average_value}), 200
        else:
            return jsonify({"error": "No value"}), 404
    else:
        return jsonify({"error": "Sensor not found"}), 404


# Да се върнат всички отчетени стойности над посочената стойност <value> за даден сензор.
# Заявката не приема тяло.
# Заявката връща списък с всички отчетени стойности над определената стойност <value> за подадения сензор.
@app.route("/sensors/<sensor_id>/data/filter/<value>", methods=["GET"])
def get_air_quality_sensor_data_above_value(sensor_id, value):
    air_sensor = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if air_sensor:
        greater_air_sensor = air_quality_sensor_collection.find({"_id": ObjectId(sensor_id), "value": {"$gt": float(value)}})
        sorted_sensor_list = list(greater_air_sensor)
        return jsonify({"Values": json_util.dumps(sorted_sensor_list)}), 200
    else:
        return jsonify({"error": "Sensor not found"}), 404


# Да се върнат последните отчетени <n> на брой стойности за даден сензор.
# Заявката не приема тяло.
# Заявката връща списък с последните <n> на брой стойности за дадения сензор.
@app.route("/sensors/<sensor_id>/data/limit/<int:n>", methods=["GET"])
def get_air_quality_sensor_data_last_n_entries(sensor_id, n):
    air_sensor = air_quality_sensor_collection.find_one({"_id": ObjectId(sensor_id)})
    if air_sensor:
        limit_air_sensor = air_quality_sensor_collection.find({"_id": ObjectId(sensor_id)}).sort("_id", -1).limit(int(n))
        limit_sensor_list = list(limit_air_sensor)
    return jsonify({"Air sensor sorted data": limit_sensor_list}), 200


if __name__ == "__main__":
    database = get_database()
    air_quality_sensor_collection = database.get_collection("air_quality_sensors")
    air_quality_sensor_data_collection = database.get_collection("air_quality_sensor_data")
    app.run(debug=True, port=8000)