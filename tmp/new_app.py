#from flask import Flask
#server = Flask('my app')
from keras.layers import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM, GRU
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import load_model
import tensorflow as tf
lstm = load_model("../data/phase-02/lstm.h5")
lstm._make_predict_function()
from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import json
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

file = open("../data/phase-02/phase-02.geojson")
tiles_geojson = json.load(file)
df = pd.read_csv("../data/phase-02/m.csv", dtype={"id": str})
mdf = pd.read_csv("../data/phase-02/harvested.csv")
mapbox_token = 'pk.eyJ1IjoibWFoZXNoeCIsImEiOiJjazJsNnlwcmQwNDFjM2xtdWNoM244emU4In0.YBO8xPG8Iw-BfL8sxSkpTw'

app = dash.Dash('sdthon')
server = app.server

df_sum = df.groupby(['id'])['harvested'].sum()
print(max(df_sum))
print(min(df_sum))
print(df_sum.head())
df_sum = df_sum.to_frame()
print(df_sum)
df_sum.columns = ['harvested']

figureMap = go.Figure(go.Choroplethmapbox(geojson=tiles_geojson,
                                          locations=df_sum.index,
                                          z=df_sum.harvested,
                                          colorscale="Viridis",
                                          zmin=17443,
                                          zmax=2962745,
                                          #zmin=0,
                                          #zmax=166448,
                                          marker_opacity=0.5,
                                          marker_line_width=0))

figureMap.update_layout(title = "Harvested Sugar Cane Area (ha) by Tile",
                        #mapbox_style="carto-positron",
                        mapbox_style="satellite",
                        mapbox_accesstoken=mapbox_token,
                        mapbox_zoom=7.5,
                        mapbox_center = {"lat": -20.4168, "lon": 148.356})

#df = pd.read_csv("../data/phase-02/m.csv")
df['harvested'] = df['harvested'] * 100 / 10000
print(max(df['harvested']))
print(min(df['harvested']))
df = df[df['cc_p80_perc'] < 35]
df = df.reset_index()
df['cc_p80_perc'] = df['cc_p80_perc']/100

# dropdown options
tiles = df.tile.unique()
opts = [{'label' : i, 'value' : i} for i in tiles]

# Step 3. Create a plotly figure
#print(opts[0]['label'])
#print(type(df.tile[0]))
initial_tile = opts[0]['label']

#fig.data = []
df2 = df[(df.tile == initial_tile)]
trace_1 = go.Scatter(x = df2.date, y = df2['ndvi'],
                     name = 'NDVI (vegetation index)',
                     mode = 'lines+markers',
                     line = dict(width = 2, color = 'rgb(0, 255, 0)'))

trace_2 = go.Scatter(x = df2.date, y = df2['cc_p80_perc'],
                     name = 'Cloud Cover (P > 0.8)',
                     mode = 'lines+markers',
                     line = dict(width = 2, color = 'gray', dash = 'dash'))

trace_3 = go.Scatter(x = df2.date, y = df2['harvested'],
                     name = 'Harvested (ha.)',
                     mode = 'lines+markers',
                     line = dict(width = 2, color = 'rgb(0, 0, 255)'))

layout = go.Layout(title = 'Time Series Plot', hovermode = 'closest')
fig = go.Figure(data = [], layout = layout)
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.update_layout(title=f"Tile={initial_tile}")
fig.update_xaxes(title_text="<b>Month</b>")
# Set y-axes titles
fig.update_yaxes(title_text="<b>ndvi & cloud cover</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>harvested</b>", secondary_y=True)

fig.add_trace( trace_1, secondary_y=False,)
fig.add_trace( trace_2, secondary_y=False,)
fig.add_trace( trace_3, secondary_y=True,)

# Set x-axis title
#fig.update_xaxes(title_text="<b>Time</b>")

app.layout = html.Div([
        html.Div([
        dcc.Graph(id='plot1', figure=figureMap)], style={'width':"50%", 'display':'inline-block'}),
        html.Div([
        dcc.Graph(id = 'plot', figure = fig)], style = {'width': "50%", 'display': 'inline-block'}),


        html.Div([
        dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=dt(2019, 11, 21),
        max_date_allowed=dt(2024, 11, 21),
        initial_visible_month=dt(2019, 12, 22),
        date=str(dt(2019,12, 22))
        ),
        html.Div(id='output-container-date-picker-single'),
        ], style= {'width': '800px'}),
        html.Div([
        dcc.Dropdown(id = 'opt', options = opts),
        html.Div(id='text1'),
        ], style={'display': 'none'}),

    ])

@app.callback(
    Output('output-container-date-picker-single', 'children'),
    [Input('my-date-picker-single', 'date'),
    Input('opt', 'value')])
def update_output(date, value):
    if date is not None:
        date = dt.strptime(date.split(' ')[0], '%Y-%m-%d')
        date_string = '2017-06-20' #date.strftime('%Y-%m-%d')
    if value is not None:
        tilex = value
        a, b = value.split('_')
    for (i, row) in mdf.iterrows():
        if row['date'] == date_string and row['x'] == a and row['y'] == b:
            test = (mdf['harvested'])[i - 12:i]
            y_true = mdf['harvested'][i]

    test = np.array(test)
    test = np.reshape(test, (test.shape[0], 1))

    # scaling data

    scaled_test = 6.007882341632221e-06 * test - 166448.0 * 6.007882341632221e-06

    predicted = lstm.predict(np.array([scaled_test]))
    y_pred = (predicted + 166448.0 * 6.007882341632221e-06) / 6.007882341632221e-06

    #xyz = str()
    return y_pred[0][0]#, y_true





@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value')])
def update_figure(value):
    fig.data = []
    df2 = df[(df.tile == value)]
    trace_1 = go.Scatter(x = df2.date, y = df2['ndvi'],
                        name = 'NDVI (vegetation index)',
                        mode = 'lines+markers',
                        line = dict(width = 2, color = 'rgb(0, 255, 0)'))

    trace_2 = go.Scatter(x = df2.date, y = df2['cc_p80_perc'],
                        name = 'Cloud Cover (P > 0.8)',
                        mode = 'lines+markers',
                        line = dict(width = 2, color = 'gray', dash = 'dash'))
    # https://community.plot.ly/t/changing-line-from-solid-to-dashed-after-certain-number/14893

    trace_3 = go.Scatter(x = df2.date, y = df2['harvested'],
                        name = 'Harvested (ha.)',
                        mode = 'lines+markers',
                        line = dict(width = 2, color = 'rgb(0, 0, 255)'))

    fig.update_layout(title=f"Tile={value}")
    fig.add_trace( go.Scatter(trace_1), secondary_y=False,)
    fig.add_trace( go.Scatter(trace_2), secondary_y=False,)
    fig.add_trace( go.Scatter(trace_3), secondary_y=True,)

    return fig

@app.callback(Output('opt', 'value'), [Input('plot1', 'hoverData')] )
def text_callback(hoverData):
    if hoverData is None:
        print(initial_tile)
        return initial_tile
    else:
        print(hoverData)
        x = hoverData["points"][0]["location"]
        #print(type(df['id'][0]))
        #print(df.loc[df['id'] == x, 'tile'])
        y = df.loc[df['id'] == x, 'tile'].iloc[0]
        #print(type(df['id'][0]))
        return y

if __name__ == '__main__':
    app.run_server(debug=True)
