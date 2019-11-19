import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import json
import plotly.graph_objs as go

app = dash.Dash(__name__)
server = app.server

mapbox_access_token = "pk.eyJ1IjoibWFoZXNoeCIsImEiOiJjazJsNnlwcmQwNDFjM2xtdWNoM244emU4In0.YBO8xPG8Iw-BfL8sxSkpTw"

#os.chdir("/home/ubuntu/app")

file = open("../data/phase-02/phase-02.geojson")
tiles = json.load(file)

df = pd.read_csv("../data/1_raw/dates.csv")
df = df.iloc[::3,:]
df = df.reset_index()
print(df)

#df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
m = pd.read_csv("../data/phase-02/m.csv", dtype={"id": str})
m['harvested'] = m['harvested'] * 100 / 10000
#m = m[m['date'] == '2016-12-22']
#df = m
#https://community.plot.ly/t/solved-scattermapbox-callback-to-update-link-not-working/20318

fig2 = dict(data=[dict(type='bar', x=m['date'], y=m['harvested'])])


marks={i: d[2:7] for i, d in enumerate(df['date'].unique())}
print(marks)

app.layout = html.Div([
    html.Div([
    dcc.Graph(id='graph-with-slider')], style={'width':'800px', 'height':'400px'}),
    html.Div([
    dcc.Slider(
        id='date-slider',
        min=0,
        max=df.shape[0],
        value=0,
        step=1,
        marks={i: d[2:7] for i, d in enumerate(df['date'].unique())}
        #vertical=True
    )
    ],
    style={'width':'800px', 'margin': 25}
    ),
    html.Div([
       dcc.Graph(id='plot2', figure=fig2),
    ], style= {'width': '800px'})
])
    


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_figure(selected_date):
    d = df.loc[selected_date,'date']
    fdf = m[m.date == d]
    map = go.Choroplethmapbox(geojson=tiles,
                        locations=fdf.id,
                        z=fdf.harvested,
                        colorscale="Viridis",
                        zmin=0,
                        zmax=1664.48,
                        text = fdf['tile'],
                        hovertemplate = '<b>Tile</b>: <b>%{text}</b>'+
                                        '<br><b> Harvested </b>: %{z}<br>',
                        marker_opacity=0.5,
                        marker_line_width=0.5,
                        name="sugar cane tile")

    return {
        'data': [map],
        'layout': go.Layout(title="plot",
                            mapbox_style="carto-positron",
                            mapbox_zoom=8,
                            mapbox_center = {"lat": -20.4168,
                                             "lon": 148.456},
                            margin={"r":0,"t":0,"l":0,"b":0},
                            width=800,
                            height=400
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)

#https://community.plot.ly/t/adding-maps-without-using-mapbox/9584/5
