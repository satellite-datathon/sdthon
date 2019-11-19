from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
import flask
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from app1 import app as app1
from app2 import app as app2

app = Dash(__name__)
#server = flask.Flask(__name__)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
html.Div(id='page-content')])

dash_app1 = Dash(__name__, server=server, url_base_pathname='/dashboard/')
dash_app2 = Dash(__name__, server=server, url_base_pathname='/reports/')
dash_app1.layout = app1.layout
dash_app2.layout = app2.layout


@server.route('/dashboard/')
def render_dashboard():
   return flask.redirect('/dash1')

@server.route('/reports/')
def render_reports():
    return flask.redirect('/dash2')

app = DispatcherMiddleware(server, { '/dash1': dash_app1.server, '/dash2': dash_app2.server})

run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
