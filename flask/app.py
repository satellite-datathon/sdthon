import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

#import run
#import app1, app2
from app1 import app as app1
from app2 import app as app2
#import server
from flask import Flask, render_template

#server=Flask(__name__)
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
                  dcc.Location(id='url', refresh=False),
                  html.Div(id='page-content')])

@app.callback(Output('page-content', 'children'),
[Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/about':
        return about()
    else: return '404'

@server.route('/about/')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run_server(debug=True)
