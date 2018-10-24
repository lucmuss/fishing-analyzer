# coding: utf-8

from mainapp import app

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import environment
from apps import statistics
from apps import histograms
from apps import distributions

main_navigation_bar = html.Div(className='container mt-2', children=[

    html.Div(className="row ml-2", children=[
        html.Img(className="rounded", src='/assets/main_logo.jpg', width='100', height='100')],
             ),

    html.Div(className="row mt-2", children=[
        html.Ul(
            id='main_navigation',
            className='nav',
            children=[
                html.Li(className='nav-item',
                        children=dcc.Link('Month Statistics',
                                          className='nav-link',
                                          href='/apps/statistics')),
                html.Li(className='nav-item',
                        children=dcc.Link('Environmental Data',
                                          className='nav-link',
                                          href='/apps/environment')),
                html.Li(className='nav-item',
                        children=dcc.Link('Histograms',
                                          className='nav-link',
                                          href='/apps/histograms')),
                html.Li(className='nav-item',
                        children=dcc.Link('Distributions',
                                          className='nav-link',
                                          href='/apps/distributions')),
            ],
        )]
             ),

])

layout = html.Div([

    main_navigation_bar,

    dcc.Location(id='url', refresh=False),
    html.Div(className='container mt-4', id='page_content')
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
