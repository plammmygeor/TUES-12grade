import pandas as pd
import plotly.express as px

from bson import ObjectId
from pymongo import MongoClient
from dash import Dash, html, callback, Output, Input, dash_table, dcc

DATABASE_NAME = "dash-exam"
CONNECTION_STRING = ""

app = Dash(__name__)

app.layout = html.Div(id="html-div", children=[
    html.H2(children="temp table"),
    dash_table.DataTable(id="sensor-table"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H2(children="temp data"),
    dcc.Graph(id='sensor-data'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
])

@app.callback(
    [
        Output("sensor-table", "data"),
        Output("sensor-data", "figure"),
    ], 
    [
        Input("interval", "n_intervals")
    ]
)
def update(_):
    sensors = list(thermometer_collection.find({}))
    data = list(temperature_collection.find({}))
    
    for sensor in sensors:
        sensor["_id"] = str(sensor["_id"])
        
    df = pd.DataFrame(data)
    fig = px.line(df, x="timestamp", y="value", color="thermometer_id")
    
    return sensors, fig

if __name__ == "__main__":
    mongo_client = MongoClient(CONNECTION_STRING)
    database = mongo_client.get_database(DATABASE_NAME)
    thermometer_collection = database.get_collection("thermometers")
    temperature_collection = database.get_collection("temperatures")
    app.run_server(debug=True)
