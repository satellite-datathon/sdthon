from flask import Flask
server = Flask('my app')

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

file = open("../data/phase-02/phase-02.geojson")
counties = json.load(file)
df = pd.read_csv("../data/phase-02/m.csv", dtype={"id": str})

mapbox_token = 'pk.eyJ1IjoibWFoZXNoeCIsImEiOiJjazJsNnlwcmQwNDFjM2xtdWNoM244emU4In0.YBO8xPG8Iw-BfL8sxSkpTw'

app = dash.Dash('sdthon')

fig1 = go.Figure(go.Choroplethmapbox(geojson=counties,  locations=df.id, z=df.harvested,
                                    colorscale="Viridis", zmin=0, zmax=166448,
                                    marker_opacity=0.5, marker_line_width=0))

fig1.update_layout(mapbox_style="carto-positron", mapbox_accesstoken=mapbox_token,  mapbox_zoom=7,
                mapbox_center = {"lat": -20.3168, "lon": 148.356})
#
# fig1.show()

dx = df.tile.unique()
opts = [{'label' : i, 'value' : i} for i in dx]
df['Date'] = pd.to_datetime(df.date)
st2 = df[(df.tile == opts[0])]
    # updating the plot
trace_1 = go.Scatter(x = st2.Date, y = st2['ndvi'],
                        name = 'ndvi',
                        line = dict(width = 2,
                                    color = 'rgb(255, 0, 0)'))
trace_2 = go.Scatter(x = st2.Date, y = st2['cc_p80_perc'],
                        name = 'cc',
                        line = dict(width = 2,
                                    color = 'rgb(0, 255, 0)'))
trace_3 = go.Scatter(x = st2.Date, y = st2['harvested'],
                        name = 'harvested',
                        line = dict(width = 2,
                                    color = 'rgb(0, 0, 255)'))
layout = go.Layout(title = 'Time Series Plot', hovermode = 'closest')
fig = go.Figure(data = [trace_1, trace_2], layout = layout)
fig = make_subplots(specs=[[{"secondary_y": True}]])
# Set x-axis title
fig.update_xaxes(title_text="<b>Date and Time</b>")
# Set y-axes titles
fig.update_yaxes(title_text="<b>ndvi & CC</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>harvested</b>", secondary_y=True)




fig2 = dict(data=[dict(type='bar', x=df['date'], y=df['harvested'])])

app.layout = html.Div([
        dcc.Graph(id='plot1', figure=fig1),
        dcc.Graph(id = 'plot', figure = fig),

        html.Div([
        dcc.Dropdown(id = 'opt', options = opts, value = '1'),
        html.Div(id='text1'),
        ], style={'display': 'none'}),

    ])

@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value')])
def update_figure(value):
    fig.data = []
    st2 = df[(df.tile == value)]
    trace_1 = go.Scatter(x = st2.Date, y = st2['ndvi'],
                        name = 'ndvi', line = dict(width = 2, color = 'rgb(255, 0, 0)'))
    trace_2 = go.Scatter(x = st2.Date, y = st2['cc_p80_perc'],
                        name = 'cc', line = dict(width = 2, color = 'rgb(0, 255, 0)'))
    trace_3 = go.Scatter(x = st2.Date, y = st2['harvested'],
                        name = 'harvested', line = dict(width = 2,color = 'rgb(0, 0, 255)'))
    fig.add_trace(go.Scatter(trace_1),secondary_y=False,)
    fig.add_trace(go.Scatter(trace_2),secondary_y=False,)
    fig.add_trace(go.Scatter(trace_3),secondary_y=True,)
    return fig

@app.callback(Output('opt', 'value'), [Input('plot1', 'hoverData')] )
def text_callback(hoverData):
    if hoverData is None:
        return 'Empty'
    else:
        x = hoverData["points"][0]["location"]
        y = df.loc[df['id'] == x, 'tile'].iloc[0]
        return y #hoverData["points"][0]["pointNumber"]

if __name__ == '__main__':
    app.run_server(debug=True)
