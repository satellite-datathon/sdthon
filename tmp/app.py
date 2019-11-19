#from flask import Flask
#server = Flask('my app')

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
server = app.server

figureMap = go.Figure(go.Choroplethmapbox(geojson=counties,  locations=df.id, z=df.harvested,
                                    colorscale="Viridis", zmin=0, zmax=166448,
                                    marker_opacity=0.5, marker_line_width=0))

figureMap.update_layout(mapbox_style="carto-positron", mapbox_accesstoken=mapbox_token,
                   mapbox_zoom=7, mapbox_center = {"lat": -20.3168, "lon": 148.356})

df = pd.read_csv("../data/phase-02/m.csv")
df['harvested'] = df['harvested'] * 100 / 10000
df = df[df['cc_p80_perc'] < 35]
df = df.reset_index()
df['cc_p80_perc'] = df['cc_p80_perc']/100 

# dropdown options
tiles = df.tile.unique()
opts = [{'label' : i, 'value' : i} for i in tiles]

# Step 3. Create a plotly figure
df2 = df[(df.tile == opts[0])]
    # updating the plot
trace_1 = go.Scatter(x = df2.date, y = df2['ndvi'],
                        name = 'ndvi',
                        line = dict(width = 2, color = 'rgb(255, 0, 0)'))
trace_2 = go.Scatter(x = df2.date, y = df2['cc_p80_perc'],
                        name = 'cloud cover (P > 0.8)',
                        line = dict(width = 2, color = 'rgb(0, 255, 0)'))
trace_3 = go.Scatter(x = df2.date, y = df2['harvested'],
                        name = 'harvested',
                        line = dict(width = 2, color = 'rgb(0, 0, 255)'))
layout = go.Layout(title = 'Time Series Plot', hovermode = 'closest')

fig = go.Figure(data = [trace_1, trace_2], layout = layout)

fig = make_subplots(specs=[[{"secondary_y": True}]])



# Set x-axis title
fig.update_xaxes(title_text="<b>Time</b>")

# Set y-axes titles
fig.update_yaxes(title_text="<b>ndvi & cloud cover</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>harvested</b>", secondary_y=True)
app.layout = html.Div([
        html.Div([
        dcc.Graph(id='plot1', figure=figureMap)], style={'width':"50%", 'display':'inline-block'}),
        html.Div([
        dcc.Graph(id = 'plot', figure = fig)], style = {'width': "50%", 'display': 'inline-block'}),

        html.Div([
        dcc.Dropdown(id = 'opt', options = opts),
        html.Div(id='text1'),
        ])#, style={'display': 'none'}),

    ])

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

    fig.add_trace( go.Scatter(trace_1), secondary_y=False,)
    fig.add_trace( go.Scatter(trace_2), secondary_y=False,)
    fig.add_trace( go.Scatter(trace_3), secondary_y=True,)

    return fig

@app.callback(Output('opt', 'value'), [Input('plot1', 'hoverData')] )
def text_callback(hoverData):
    if hoverData is None:
        return 'Empty'
    else:
        x = hoverData["points"][0]["location"]
        print(type(x))
        y = df.loc[df['id'] == x, 'tile'].iloc[0]
        print(type(df['id'][0]))
        return y

if __name__ == '__main__':
    app.run_server(debug=True)
