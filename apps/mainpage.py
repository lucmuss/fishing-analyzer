# coding: utf-8

import datetime

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import config
from mainapp import app

default_description: str = """My project ...."""

layout = html.Div(
    children=[
        html.Div(children=[html.P(children=default_description)]),
    ]
)
