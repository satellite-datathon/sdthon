import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Step 1. Launch the application
app = dash.Dash()
server=app.server

# Step 2. Import the dataset
df = pd.read_csv("../data/phase-02/m.csv")
df['harvested'] = df['harvested'] * 100 / 10000
df = df[df['cc_p80_perc'] < 35]
df['cc_p80_perc'] = df['cc_p80_perc']/100 

# dropdown options
tiles = df.tile.unique()
opts = [{'label' : i, 'value' : i} for i in tiles]

# Step 3. Create a plotly figure
df2 = df[(df.tile == opts[0])]
    # updating the plot
trace_1 = go.Scatter(x = df2.date, y = df2['ndvi'],
                        name = 'ndvi',
                        line = dict(width = 2,
                                    color = 'rgb(255, 0, 0)'))
trace_2 = go.Scatter(x = df2.date, y = df2['cc_p80_perc'],
                        name = 'cloud cover (P > 0.8)',
                        line = dict(width = 2,
                                    color = 'rgb(0, 255, 0)'))
trace_3 = go.Scatter(x = df2.date, y = df2['harvested'],
                        name = 'harvested',
                        line = dict(width = 2,
                                    color = 'rgb(0, 0, 255)'))
layout = go.Layout(title = 'Time Series Plot',
                   hovermode = 'closest')

fig = go.Figure(data = [trace_1, trace_2], layout = layout)

fig = make_subplots(specs=[[{"secondary_y": True}]])



# Set x-axis title
fig.update_xaxes(title_text="<b>Time</b>")

# Set y-axes titles
fig.update_yaxes(title_text="<b>ndvi & cloud cover</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>harvested</b>", secondary_y=True)

# Step 4. Create a Dash layout
app.layout = html.Div([
                html.P([
                     html.Label("Choose a Tile"),
                                  dcc.Dropdown(id = 'opt', options = opts, value = '1536_1536')
                ], style = {'width': '400px',
                            'fontSize' : '20px',
                            'padding-left' : '100px',
                            'display': 'inline-block'}),
                html.Div([
                dcc.Graph(id = 'plot', figure = fig),
                ], style = {'width': '800px'})
             ])


# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value')])
def update_figure(value):
    fig.data = []
    df2 = df[(df.tile == value)]
    trace_1 = go.Scatter(x = df2.date, y = df2['ndvi'],
                        name = 'NDVI (vegetation index)',
                        mode = 'lines+markers',
                        line = dict(width = 2,
                                    color = 'rgb(0, 255, 0)'))
     
    trace_2 = go.Scatter(x = df2.date, y = df2['cc_p80_perc'],
                        name = 'Cloud Cover (P > 0.8)',
                        mode = 'lines+markers',
                        line = dict(width = 2,
                                    color = 'gray',
                                    dash = 'dash'))
    # https://community.plot.ly/t/changing-line-from-solid-to-dashed-after-certain-number/14893
     
    trace_3 = go.Scatter(x = df2.date, y = df2['harvested'],
                        name = 'Harvested (ha.)',
                        mode = 'lines+markers',
                        line = dict(width = 2,
                                    color = 'rgb(0, 0, 255)'))
    #fig = go.Figure(data = [trace_1, trace_2, trace_3], layout = layout)

    # Add traces
    fig.add_trace(
        go.Scatter(trace_1),
        secondary_y=False,
    )

    
    # Add traces
    
    fig.add_trace(
        go.Scatter(trace_2),
        secondary_y=False,
    )
     

    fig.add_trace(
        go.Scatter(trace_3),
        secondary_y=True,
    )

    return fig

# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug = True)
