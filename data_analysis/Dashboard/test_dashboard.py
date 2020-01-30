import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from datetime import datetime as dt
from datetime import  timedelta
from pytz import timezone
import copy
import re

import pathlib

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.config.suppress_callback_exceptions = True

# get relative data folder
PATH = pathlib.Path(__file__).parent

DATA_PATH = PATH.joinpath("data").resolve()

def description():
    return html.P(
        children=[
            """
    - Choose metric
    - Select date range 
    - Get data from database 
    - Play with plots
    """
        ],
        className="description-sidebar",
    )

app.layout = html.Div(
    children=[
        html.Div(
            [
                #html.Img(  Cybera logo?
                #    src=app.get_asset_url("dash-logo.png"), className="plotly-logo"
                #),
                html.H1(children="ConnectIn"),
                description(),
                html.Div(
                    # Empty child function for the callback - save intermediate data
                    html.Div(id="demo-explanation", children=[])
                ),
                html.Div(
                    [
                        html.H6("Metric"),
                        html.Div(
                            [
                                dcc.Dropdown(
                                options=[
                                    {'label': 'Upload speed', 'value': 'UPLOAD'},
                                    {'label': 'Download speed', 'value': 'DOWNLOAD'},
                                    {'label': 'Ping latency', 'value': 'PING'}
                                ],
                                 value='DOWNLOAD',
                                 style={
                                     "width": "81%",
                                      "display": "inline-block",
                                      "margin": "0 auto",
                                      "textAlign": "center",
                                      "font-family": "Geneva",
                                      "color": "#407DFA",
                                      #"color": "#8898B2",
                                      "backgroundColor": "#01183A",
                                      "background": "#01183A"
                                 }
                                 ),
                            ],className="test_dropdown",
                        ),
                    ],
                   # className="metric_dropdown",
                ),
                html.Div(
                    [
                    html.Div(
                            [
                                html.Br(),
                               # html.Br(),
                                html.H6("Date"),
                                dcc.RadioItems(
                                options=[
                                {'label': 'Range', 'value': 'RANGE'},
                                {'label': 'From/To', 'value': 'FROMTO'}
                                 ],
                                value='RANGE',
                                labelStyle={'display': 'inline-block'}
                                ),
                            ]
                        ),
                    html.Div(
                        [
                        dcc.Dropdown(
                                options=[
                                    {'label': 'Last 6 months', 'value': '6'},
                                    {'label': 'Last year', 'value': '12'},
                                    {'label': 'All data', 'value': '0'}
                                ],
                                 value='12',
                                 style={
                                     "width": "81%",
                                      "display": "inline-block",
                                      "margin": "0 auto",
                                      "textAlign": "center",
                                      "font-family": "Geneva",
                                       "color": "#407DFA",
                                    #  "color": "#8898B2",
                                     # "color": "#D1D1D1",
                                      "backgroundColor": "#01183A",
                                   #   "background": "#01183A"
                                 }
                                 ),
                            ],className="test_dropdown",
                     ),
                    html.Br(),
                    html.Br(),
                    html.Div(
                        [
                        dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=dt(1997, 5, 3),
                        end_date_placeholder_text='Select a date!',
                        style={
                                     "width": "80%",
                                     "display": "inline-block",
                                      "margin": "0 auto",
                                      "textAlign": "center",
                                     #"font-family": "Geneva",
                                      #"color": "#407DFA",
                                      #"color": "#8898B2",
                                     # "backgroundColor": "#01183A",
                                      "background": "#01183A",
                                      #border: 1px solid  # 555;
                                 }
                        )
                        ]
                    ),
                    ],
                    className="date_selection",
                ),
                html.Br(),
                html.Button(
                    "Get data", id="button-db", className="button_submit"
                ),
                html.Br(),
            ],
            className="four columns instruction",
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="connectin-tabs",
                    value="raw-tab",
                    children=[
                        dcc.Tab(label="RAW DATA", value="raw-tab"),
                        dcc.Tab(label="AGGREAGTED DATA", value="agg-tab"),
                        dcc.Tab(label="MAP AND STATISTICS", value="map-tab"),
                    ],
                    className="tabs",
                ),
                html.Div(
                    id="connectin-tabs-content",
                    className="canvas",
                    #style={"text-align": "left", "margin": "auto"},
                ),
              #  html.Div(className="upload_zone", id="upload-stitch", children=[]),
              #  html.Div(id="sh_x", hidden=True),
              #  html.Div(id="stitched-res", hidden=True),
                dcc.Store(id="memory-df"),
            ],
            className="eight columns result",
        ),
    ],
    className="row twelve columns",
)

@app.callback(Output('connectin-tabs-content', 'children'),
              [Input('connectin-tabs', 'value')])
def render_content(tab):
    if tab == 'raw-tab':
        return html.Div([
            html.Div(
            dcc.RadioItems(
                options=[
                    {'label': 'Speedtest', 'value': 'SPEEDTEST'},
                    {'label': 'Iperf', 'value': 'IPERF'}
                ],
                value='SPEEDTEST',
                labelStyle={'display': 'inline-block'}
            ),style={'width': '30%', 'display': 'inline-block'}),
            html.Div(
            dcc.Dropdown(
                options=[
                    {'label': 'All devices', 'value': 'ALL'},
                    {'label': '1', 'value': '1'},
                ],
                value='DOWNLOAD'),
             style={'width': '30%', 'display': 'inline-block'}),
        ])
    #elif tab == 'tab-2':
    #    return html.Div([
    #        html.H3('Tab content 2')
    #    ])


if __name__ == "__main__":
    app.run_server(debug=True)
