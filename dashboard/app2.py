import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly
import settings
import pymysql
import datetime

# pip install pyorbital
from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):

    return [html.P(children = n)]
if __name__ == '__main__':
    app.run_server(debug=True)