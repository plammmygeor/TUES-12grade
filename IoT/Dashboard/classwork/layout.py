from pymongo import MongoClient
from dash import Dash, dcc, html, Input, Output, callback, dash_table

URI = "mongodb+srv://plamenavgeorgieva2019:ZGQh6Z2y9qB52p5y@tues-iot.kgcueop.mongodb.net/?retryWrites=true&w=majority&appName=TUES-IoT"

app = Dash(__name__)
app.layout = html.Div([
    html.H4("Live temperature feed"),
    dash_table.DataTable(id="sensor-update-table", page_size=100),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
])