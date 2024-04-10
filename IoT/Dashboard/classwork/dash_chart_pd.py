from pymongo import MongoClient
from dash import Dash, html, callback, Output, Input, dash_table, dcc
import plotly.express as px
import pandas as pd
import certifi
from bson import ObjectId

DATABASE_NAME = "dash-exercise"
CONNECTION_STRING = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

mongo_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
database = mongo_client.get_database(DATABASE_NAME)

air_quality_sensor_collection = database.get_collection("air_quality_sensors")
air_quality_sensor_data_collection = database.get_collection("air_quality_sensor_data")

app = Dash(__name__)

sensor_options = [{'label': 'Sensor ID ' + str(i['_id']), 'value': str(i['_id'])} for i in air_quality_sensor_collection.find({})]

app.layout = html.Div([
    html.H2(children="Air quality sensor chart"),
    dcc.RadioItems(
        id='sensor-id-selector',
        options=sensor_options,
        value=str(air_quality_sensor_collection.find_one()['_id'])  
    ),
    dcc.Graph(id='sensor-chart'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H2(children="Air quality sensor table"),
    dash_table.DataTable(id="sensor-table"),
    html.Br(),
    html.Br(),
    html.Br(),
    dash_table.DataTable(id="sensor-data-table"),
    dcc.Interval(id="interval", interval=1000, n_intervals=0)
])

@app.callback(
    [
        Output("sensor-chart", "figure"),
        Output("sensor-table", "data"),
        Output("sensor-data-table", "data"),
    ], 
    [
        Input("sensor-id-selector", "value"),
        Input("interval", "n_intervals")
    ]
)
def update_info(selected_sensor_id, _):
    sensors = list(air_quality_sensor_collection.find({"_id": selected_sensor_id}))
    sensor_data = list(air_quality_sensor_data_collection.find({"air_quality_sensor_id": selected_sensor_id}))
    
    for sensor in sensors:
        sensor["_id"] = str(sensor["_id"])
    for data in sensor_data:
        data["_id"] = str(data["_id"])
        data["air_quality_sensor_id"] = str(data["air_quality_sensor_id"])
    
    df = pd.DataFrame(sensor_data)
    fig = px.line(df, x="value", y="timestamp", title=f"Sensor ID: {selected_sensor_id}")
    
    return fig, sensors, sensor_data

if __name__ == "__main__":
    app.run(debug=True, port=8888)
