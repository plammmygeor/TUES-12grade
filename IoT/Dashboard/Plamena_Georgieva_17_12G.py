import pandas as pd
import plotly.express as px

from bson import ObjectId
from pymongo import MongoClient
from dash import Dash, html, callback, Output, Input, dash_table, dcc

DATABASE_NAME = "dash-exam"
CONNECTION_STRING = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

app = Dash(__name__)

mongo_client = MongoClient(CONNECTION_STRING)
database = mongo_client.get_database(DATABASE_NAME)
thermometer_collection = database.get_collection("thermometers")
temperature_collection = database.get_collection("temperatures")

def get_sensor_options():
    return [{'label': 'All', 'value': 'All'}] + [{'label': 'Thermometer ID ' + str(i['_id']), 'value': str(i['_id'])} for i in thermometer_collection.find({})]

app.layout = html.Div(id="html-div", children=[
    html.H2(children="Temperature Table"),
    dash_table.DataTable(id="sensor-table"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H2(children="Temperature Data Chart"),
    dcc.Graph(id='sensor-data'),
    dcc.RadioItems(
        id='sensor-id-selector',
        options=get_sensor_options(),
        value='All'  
    ),
    dcc.Interval(id="interval", interval=1000, n_intervals=0)
])

@app.callback(
    [
        Output("sensor-table", "data"),
        Output("sensor-data", "figure"),
    ], 
    [
        Input("interval", "n_intervals"),
        Input("sensor-id-selector", "value")
    ]
)

def update_info(_, selected_sensor_id):
    if selected_sensor_id == 'All':
        temp_data = list(temperature_collection.find({}))
    else:
        temp_data = list(temperature_collection.find({"thermometer_id": ObjectId(selected_sensor_id)}))
    
    termo_sensors = list(thermometer_collection.find({}))
    
    for sensor in termo_sensors:
        sensor["_id"] = str(sensor["_id"])
        
    df = pd.DataFrame(temp_data)
    fig = px.line(df, x="timestamp", y="value", color="thermometer_id")
    
    return termo_sensors, fig

if __name__ == "__main__":
    app.run(debug=True, port=8050)
