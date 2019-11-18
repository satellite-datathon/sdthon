import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import json
file = open("../data/phase-02/phase-02.geojson")
tiles = json.load(file)
import pandas as pd
df = pd.read_csv("../data/phase-02/m.csv", dtype={"id": str})
from plotly import graph_objs as go

mapbox_access_token = 'pk.eyJ1IjoibWFoZXNoeCIsImEiOiJjazJsNnlwcmQwNDFjM2xtdWNoM244emU4In0.YBO8xPG8Iw-BfL8sxSkpTw'

app = dash.Dash('sdthon')
server=app.server

#import plotly.graph_objects as go

#mapbox_access_token = open(".mapbox_token").read()
text_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)

fig = go.Figure(go.Scattermapbox(
        lat=['45.5017'],
        lon=['-73.5673'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=['Montreal'],
    ))

fig.update_layout(
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=45,
            lon=-73
        ),
        pitch=0,
        zoom=5
    )
)

#fig.show()

fig2 = dict(data=[dict(type='bar', x=df['date'], y=df['harvested'])])

app.layout = html.Div([
     html.Div([
        html.H2('satellite-datathon', style=text_style),
        dcc.Graph(id='plot1', figure=fig),
        html.Div(id='text1'),
     ], style={'width': '49%', 'display': 'inline-block'}),
     html.Div([
        dcc.Graph(id='plot2', figure=fig2),
     ], style= {'width': '49%', 'display': 'inline-block'})
    ])

@app.callback(Output('text1', 'children'), [Input('plot1', 'selectedData')] )
def text_callback(selectedData):
    if selectedData is None:
        return 'Empty'
    else:
        return selectedData


if __name__ == '__main__':
    app.run_server(debug=True)
