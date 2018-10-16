# coding: utf-8

from mainapp import app

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps.data import environment
from apps.data import statistics

main_navigation_bar = html.Div([
    html.Br(),
    dcc.Link('Go to Month Statistics', href='/apps/data/statistics'),
    html.Br(),
    dcc.Link('Go to Environmental Data', href='/apps/data/environment'),
    html.Br(),
])

layout = html.Div([

    main_navigation_bar,

    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content')
])

app.layout = layout


@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/data/environment':
        return environment.layout
    elif pathname == '/apps/data/statistics':
        return statistics.layout
    else:
        return "404"


if __name__ == '__main__':
    app.run_server(debug=True)
