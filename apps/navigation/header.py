# coding: utf-8

import dash_html_components as html
import dash_core_components as dcc

main_navigation_bar = html.Div([
    html.Br(),
    dcc.Link('Go to Month Statistics', href='/visualisation/apps/month_statistics'),
    html.Br(),
    dcc.Link('Go to Environmental Data', href='/visualisation/apps/environmental_data'),
    html.Br(),
])

layout = html.Div([

    main_navigation_bar,

    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content')
])
