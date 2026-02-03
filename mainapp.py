# coding: utf-8

import os

import dash
import flask

server: flask.Flask = flask.Flask(__name__)
server.config.from_object(__name__)
server.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app = dash.Dash(__name__, server=server)
app.config["suppress_callback_exceptions"] = True
