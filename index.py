# coding: utf-8

from mainapp import app

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import config

from apps import environment
from apps import statistics
from apps import histograms
from apps import distributions
from apps import adddata
from apps import mainpage

main_footer = main_navigation_bar = html.Div(className='container', children=[
    html.Footer(children=[
        html.P(className='',
               children='This website was created by Lucas Mußmächer in 2018 - Email: lucas.mussmaecher@gmail.com'),
    ])
])

main_navigation_bar = html.Div(className='container mt-2', children=[

    html.Div(className="row mt-4", children=[
        html.Ul(
            className='nav bg-light',
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
                html.Li(className='nav-item',
                        children=dcc.Link('Add Data',
                                          className='nav-link',
                                          href='/apps/addfish')),
                html.Li(className='nav-item',
                        children=dcc.Link('Description',
                                          className='nav-link',
                                          href='/')),
            ],
        )]
             ),

])

layout = html.Div([

    main_navigation_bar,

    dcc.Location(id='url', refresh=False),
    html.Div(className='container clearfix mt-4 mb-4', id='page_content'),

    main_footer,
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
    elif pathname == '/apps/addfish':
        return adddata.layout
    else:
        return mainpage.layout


if __name__ == '__main__':
    if config.RUN_AS_PRODUCTION:
        app.run_server(host='0.0.0.0', port=80)
    else:
        app.run_server(debug=True, port=8050)
