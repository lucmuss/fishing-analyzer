# coding: utf-8

from mainapp import app

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import environment
from apps import statistics
from apps import histograms
from apps import distributions

main_navigation_bar = html.Div([

    html.Nav(
        html.Div(
            html.Ul(
                children=[
                    html.Li(dcc.Link('Statistics', href='/apps/statistics')),
                    html.Li(dcc.Link('Environmental', href='/apps/environment')),
                    html.Li(dcc.Link('Histograms', href='/apps/histograms')),
                    html.Li(dcc.Link('Distributions', href='/apps/distributions')),
                ],
                id='main_navigation'
            )
        )
    ),

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
    if pathname == '/apps/environment':
        return environment.layout
    elif pathname == '/apps/statistics':
        return statistics.layout
    elif pathname == '/apps/histograms':
        return histograms.layout
    elif pathname == '/apps/distributions':
        return distributions.layout
    else:
        return "Main Page"


if __name__ == '__main__':
    app.run_server(debug=True)
