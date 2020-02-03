import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
from dateutil.relativedelta import relativedelta

#import pathlib
import sys
sys.path.append('/home/connectin/data_analysis/Interactive_notebooks')
from data_exploration import *

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.config.suppress_callback_exceptions = True

# get relative data folder
#PATH = pathlib.Path(__file__).parent

#DATA_PATH = PATH.joinpath("data").resolve()

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
                    html.Div(id='intermediate-value', style={'display': 'none'}) #children='Enter a value and press submit')#
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
                                 },
                                id="mes_dropdown", className="test_dropdown"
                                 ),]
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
                                labelStyle={'display': 'inline-block'},
                                id="date_radio"
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
                                 value='6',
                                style={
                                     "width": "80%",
                                      "display": "inline-block",
                                      "margin": "0 auto",
                                      "textAlign": "center",
                                      "font-family": "Geneva",
                                       "color": "#407DFA",
                                      "backgroundColor": "#01183A",
                                      "background": "#01183A"
                                 },
                            id='date_dropdown', className="test_dropdown"
                                 ),]
                     ),
                    html.Br(),
                    html.Br(),
                    html.Div(
                        [
                        dcc.DatePickerRange(
                        id='date-picker-range',
                        #initial_visible_month=datetime.today(),
                        #start_date = datetime.now().replace(microsecond=0,second=0,hour=0,minute=0)  - datetime.timedelta(months=6),
                        start_date = datetime.now() + relativedelta(months=-6),
                        end_date = datetime.now(),
                        display_format='MMM Do, YY',
                        style={
                                     # "width": "60%",
                                      "display": "none",
                                      "margin": "0 auto",
                                      "textAlign": "center",
                                      "font-family": "Geneva",
                                      "color": "#407DFA",
                                      "backgroundColor": "#01183A",
                                      "background": "#01183A"
                                 }
                        )
                        ]
                    ),
                    ],
                    className="date_selection",
                ),
                html.Br(),
                html.Button(
                    children="Get data", id="button-db", n_clicks=0, className="button_submit"
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
            html.Br(),
            html.Div([
            html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Speedtest', 'value': 'speedtest'},
                    {'label': 'Iperf', 'value': 'iperf'}
                ],
                value='speedtest',
                labelStyle={'display': 'inline-block'},
                id="speedtest_iperf_tab1",
                style={
                    'width': '70%'#,
                    #'textAlign': 'center'
                }
            )],className="four columns"),
            html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'All devices', 'value': 'ALL'},
                    {'label': '1', 'value': '1'},
                ],
                value='ALL',
                id="device_tab1",
                clearable=False,
               style={
                    'width': '70%',
                    'color': "#407DFA"
                }
            )], className="four columns"),
           ], className="row"),
            html.Div([
            html.H4('Test graph 1'),
            dcc.Graph(
                id='graph-1-tabs'
         )
         ]),

])
    #elif tab == 'tab-2':
    #    return html.Div([
    #        html.H3('Tab content 2')
    #    ])

@app.callback(Output('intermediate-value', 'children'),
              [Input('button-db', 'n_clicks')],
              [State('mes_dropdown', 'value'),
               State('date_radio', 'value'),
               State('date_dropdown', 'value'),
               State('date-picker-range', 'start_date'),
               State('date-picker-range', 'end_date')])
def get_data(n_clicks,mes_type,date_type,date_range,start_date, end_date):
     # some expensive clean data step
     client, client_df = connect_to_influxdb()
     if date_type == 'RANGE':
         df = measurment_by_range(client_df, mes_type, 0, int(date_range))
     else:
         if start_date is not None:
             start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
         else:
             start_date = 0
         if end_date is not None:
             end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
         else:
             end_date = 0
         df = measurment_by_range(client_df,mes_type,end_date,start_date)

     # more generally, this line would be
     # json.dumps(df)
     #return "clicked "+ str(n_clicks)
     return df.to_json(date_format='iso', orient='split')

@app.callback(Output('graph-1-tabs', 'figure'),
              [Input('intermediate-value', 'children'),
               Input('speedtest_iperf_tab1', 'value'),
               Input('device_tab1', 'value')])
def update_graph(jsonified_data,test_type,device):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    if jsonified_data:
        df = pd.read_json(jsonified_data, orient='split')
        if device=="ALL":
            subset = df[df["test_type"] == test_type]
        else:
            subset = df[(df["test_type"] == test_type) & (df["SK_PI"] == int(device))]
        device_numbers = subset["SK_PI"].unique()
        figure = get_fig_raw_data_6_months(subset, device_numbers)
    else:
        figure = go.Figure()
    return figure


@app.callback(Output('device_tab1', 'options'),
              [Input('intermediate-value', 'children'),
               Input('speedtest_iperf_tab1', 'value')])
def update_device_numbers(jsonified_data,test_type):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    result = [{'label': 'All devices', 'value': 'ALL'}]
    if jsonified_data:
        df = pd.read_json(jsonified_data, orient='split')
        subset = df[df["test_type"] == test_type]
        device_numbers = subset["SK_PI"].sort_values().unique()
        list1 = [{'label': str(i), 'value': str(i)} for i in device_numbers]
        result = list1+result
    return result

@app.callback(
   [Output('date-picker-range', 'style'),
    Output('date_dropdown', 'style')],
   [Input('date_radio', 'value')])

def show_hide_element(visibility_state):
    if visibility_state == 'FROMTO':
        return {#"width": "60%",
                 "display": "inline-block",
                 "margin": "0 auto",
                 "textAlign": "center",
                 "font-family": "Geneva",
                 "color": "#407DFA",
                 "backgroundColor": "#01183A",
                 "background": "#01183A"
                  },\
               {
                  "width": "80%",
                   'display': 'none',
                   "margin": "0 auto",
                   "textAlign": "center",
                   "font-family": "Geneva",
                   "color": "#407DFA",
                   "backgroundColor": "#01183A",
                   "background": "#01183A"
         }
    elif visibility_state == 'RANGE':
        return {#"width": "60%",
                "display": "none",
                 "margin": "0 auto",
                 "textAlign": "center",
                 "font-family": "Geneva",
                 "color": "#407DFA",
                 "backgroundColor": "#01183A",
                "background": "#01183A"}\
            ,{
                   "width": "80%",
                   "display": "inline-block",
                   "margin": "0 auto",
                   "textAlign": "center",
                   "font-family": "Geneva",
                   "color": "#407DFA",
                   "backgroundColor": "#01183A",
                   "background": "#01183A"
               }


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
