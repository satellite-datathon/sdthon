import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Step 1. Launch the application
app = dash.Dash()

# Step 2. Import the dataset
filepath = 'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv'
#st = pd.read_csv(filepath)
st = pd.read_csv("../data/phase-02/m.csv")

# dropdown options
# features = st.columns[1:-1]
# opts = [{'label' : i, 'value' : i} for i in features]

df = st.tile.unique()
opts = [{'label' : i, 'value' : i} for i in df]

# range slider options
st['Date'] = pd.to_datetime(st.date)
# dates = ['2015-02-17', '2015-05-17', '2015-08-17', '2015-11-17',
#          '2016-02-17', '2016-05-17', '2016-08-17', '2016-11-17', '2017-02-17']



# Step 3. Create a plotly figure
st2 = st[(st.tile == opts[0])]
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
layout = go.Layout(title = 'Time Series Plot',
                   hovermode = 'closest')

fig = go.Figure(data = [trace_1, trace_2], layout = layout)

fig = make_subplots(specs=[[{"secondary_y": True}]])



# Set x-axis title
fig.update_xaxes(title_text="<b>Date and Time</b>")

# Set y-axes titles
fig.update_yaxes(title_text="<b>ndvi & CC</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>harvested</b>", secondary_y=True)

# Step 4. Create a Dash layout
app.layout = html.Div([

                              # dropdown
                html.P([
                                  html.Label("Choose a Tile"),
                                  dcc.Dropdown(id = 'opt', options = opts,
                                              value = '1')
                                      ], style = {'width': '400px',
                                                  'fontSize' : '20px',
                                                  'padding-left' : '100px',
                                                  'display': 'inline-block'}),
                # adding a plot
                dcc.Graph(id = 'plot', figure = fig),
                #  range slider
                # html.P([
                #     html.Label("Time Period"),
                #     dcc.RangeSlider(id = 'slider',
                #                     marks = {i : dates[i] for i in range(0, 9)},
                #                     min = 0,
                #                     max = 8,
                #                     value = [1, 7])
                #         ], style = {'width' : '80%',
                #                     'fontSize' : '20px',
                #                     'padding-left' : '100px',
                #                     'display': 'inline-block'})
                      ])


# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value')])
def update_figure(value):
    fig.data = []
    # filtering the data
    #st2 = st[(st.Date > dates[input2[0]]) & (st.Date < dates[input2[1]])]
    st2 = st[(st.tile == value)]
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
