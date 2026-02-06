import datetime

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from fishing_analyzer import config
from fishing_analyzer.mainapp import app

default_description: str = """My project ...."""

layout = html.Div(
    children=[
        html.Div(children=[html.P(children=default_description)]),
    ]
)
