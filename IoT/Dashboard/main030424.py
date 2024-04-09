import json
import random
from time import time

from pymongo import MongoClient
from bson import json_util, ObjectId
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE_NAME = "mongo_exam_database"
CONNECTION_STRING = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"


@app.route("/sensors", methods=["POST"])
def create_air_quality_sensor():
    data = request.get_json()
    air_quality_sensor_collection.insert_one(data)
    return jsonify(json.loads(json_util.dumps(data))), 201


@app.route("/sensors/<sensor_id>/data", methods=["POST"])
def create_air_quality_sensor_data_entry(sensor_id):
    data = {
        "value": random.randint(0, 100),
        "timestamp": time(),
        "air_quality_sensor_id": ObjectId(sensor_id)
    }
    air_quality_sensor_data_collection.insert_one(data)
    return jsonify(json.loads(json_util.dumps(data))), 201

from pymongo import MongoClient
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import pandas as pd

URI = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

app = Dash(__name__)

app.layout = html.Div([
    html.H4("Live temperature feed"),
    dash_table.DataTable(
        id="sensor-update-table",
        page_size=100,
        columns=[{"name": i, "id": i} for i in ['value', 'timestamp', 'air_quality_sensor_id']]
    ),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
])

@app.callback (
    Output(component_id='sensor-update-table', component_property='data'),
    Input(component_id='interval-component', component_property='n_intervals')
)

def data_table(n_intervals):
    data_list = list(air_quality_sensor_data_collection.find())
    data_serializable = [{k: v if not isinstance(v, ObjectId) else str(v) for k, v in entry.items()} for entry in data_list]
    return data_serializable

    
if __name__ == "__main__":
    mongo_client = MongoClient(CONNECTION_STRING)
    database = mongo_client.get_database(DATABASE_NAME)
    air_quality_sensor_collection = database.get_collection("air_quality_sensors")
    air_quality_sensor_data_collection = database.get_collection("air_quality_sensor_data")
    app.run_server(debug=True, port=8000)
    