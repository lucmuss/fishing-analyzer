from dash import html

default_description: str = """My project ...."""

layout = html.Div(
    children=[
        html.Div(children=[html.P(children=default_description)]),
    ]
)
