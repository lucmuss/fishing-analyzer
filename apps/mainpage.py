# coding: utf-8

import datetime

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import config
from mainapp import app

default_description = '''My project ....'''

layout = html.Div(children=[

    html.Div(
        children=[
            html.P(children=default_description)
        ]),

])
