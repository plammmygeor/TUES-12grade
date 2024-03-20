import json

from flask import Flask, request, jsonify
from database import get_database
from time import time
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)


@app.route("/motion-sensors", methods=["POST"])
def create_sensor():
	pass


@app.route("/motion-sensors/<sensor_id>", methods=["PUT"])
def update_sensor(sensor_id):
	pass


@app.route("/motion-sensors/<sensor_id>", methods=["DELETE"])
def delete_sensor(sensor_id):
	pass


@app.route("/motion-sensors", methods=["GET"])
def get_all_sensors():
	pass


@app.route("/motion-sensors/<sensor_id>", methods=["GET"])
def get_sensor_by_id(sensor_id):
	pass


@app.route("/motion-sensors/<sensor_id>/data", methods=["POST"])
def create_sensor_data(sensor_id):
	pass


@app.route("/motion-sensors/<sensor_id>/data/<data_id>", methods=["DELETE"])
def delete_sensor_data(sensor_id, data_id):
	pass


@app.route("/motion-sensors/<sensor_id>/data", methods=["GET"])
def get_sensor_data(sensor_id):
	pass


if __name__ == "__main__":
	database = get_database()
	sensor_collection = database["sensors"]
	sensor_data_collection = database["sensor_data"]
	app.run(debug=True, port=5000)