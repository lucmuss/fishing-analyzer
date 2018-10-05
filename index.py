from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from dash_main_app import app
from dash_main_app import server

from dash_apps import environmental_data_app
from dash_apps import month_statistics_app

index_navigation_bar = html.Div([
    html.Br(),
    dcc.Link('Go to Month Statistics', href='/dash/apps/month_statistics'),
    html.Br(),
    dcc.Link('Go to Environmental Data', href='/dash/apps/environmental_data'),
    html.Br(),
])

app.layout = html.Div([

    index_navigation_bar,

    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content')
])


@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dash/apps/environmental_data':
        return environmental_data_app.layout
    elif pathname == '/dash/apps/month_statistics':
        return month_statistics_app.layout
    else:
        return ""


@server.route('/hello')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run_server(debug=True)
