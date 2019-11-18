from flask import Flask
server = Flask('my app')

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import json
file = open("../data/phase-02/phase-02.geojson")
counties = json.load(file)
import pandas as pd
df = pd.read_csv("../data/phase-02/m.csv", dtype={"id": str})
from plotly import graph_objs as go

mapbox_token = 'pk.eyJ1IjoibWFoZXNoeCIsImEiOiJjazJsNnlwcmQwNDFjM2xtdWNoM244emU4In0.YBO8xPG8Iw-BfL8sxSkpTw'

app = dash.Dash('sdthon')

text_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)

fig1 = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.tile, z=df.harvested,
                                    colorscale="Viridis", zmin=0, zmax=166448,
                                    marker_opacity=0.5, marker_line_width=0))

fig1.update_layout(mapbox_style="carto-positron", mapbox_accesstoken=mapbox_token,  mapbox_zoom=8,
                mapbox_center = {"lat": -20.3168, "lon": 148.356})


fig2 = dict(data=[dict(type='bar', x=df['date'], y=df['harvested'])])

app.layout = html.Div([
     html.Div([
        html.H2('satellite-datathon', style=text_style),
        dcc.Graph(id='plot1', figure=fig1),
        html.Div(id='text1'),
     ], style={'width': '50%', 'display': 'inline-block'}),
     html.Div([
        dcc.Graph(id='plot2', figure=fig2),
     ], style= {'width': '50%', 'display': 'inline-block'})
    ])

@app.callback(Output('text1', 'children'), [Input('plot1', 'selectedData')] )
def text_callback(selectedData):
    if selectedData is None:
        return 'Empty'
    else:
        return selectedData

if __name__ == '__main__':
    app.run_server(debug=True)
