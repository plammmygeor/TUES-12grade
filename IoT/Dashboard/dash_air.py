from pymongo import MongoClient
from dash import Dash, html, callback, Output, Input, dash_table, dcc

DATABASE_NAME = "dash-exercise"
CONNECTION_STRING = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

app = Dash(__name__)

app.layout = html.Div(id="html-div", children=[
    html.H2(children="Air quality sensor table"),
    dash_table.DataTable(id="sensor-table"),
    html.Br(),
    html.Br(),
    html.Br(),
    dash_table.DataTable(id="sensor-data-table"),
    dcc.Interval(id="interval", interval=1000, n_intervals=0)
])

@callback(
    [
    Output("sensor-table", "data"),
    Output("sensor-data-table", "data"),
    ], 
    [
    Input("interval", "n_intervals")
    ]
)

def update_tables_info(_):
    air_quality_sensor_collection = database.get_collection("air_quality_sensors")
    air_quality_sensor_data_collection = database.get_collection("air_quality_sensor_data")
    
    sensors = list(air_quality_sensor_collection.find({}))
    sensor_data = list(air_quality_sensor_data_collection.find({}))
    
    for sensor in sensors:
        sensor["_id"] = str(sensor["_id"])
    for data in sensor_data:
        data["_id"] = str(data["_id"])
        data["air_quality_sensor_id"] = str(data["air_quality_sensor_id"])
    
    return sensors, sensor_data


if __name__ == "__main__":
    mongo_client = MongoClient(CONNECTION_STRING)
    database = mongo_client.get_database(DATABASE_NAME)
    air_quality_sensor_collection = database.get_collection("air_quality_sensors")
    air_quality_sensor_data_collection = database.get_collection("air_quality_sensor_data")
    app.run(debug=True, port=8050)