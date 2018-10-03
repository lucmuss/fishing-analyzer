from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from dash_apps import environmental_data
from dash_apps import month_statistics

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content')
])


@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/environmental_data':
        return environmental_data.layout
    elif pathname == '/apps/month_statistics':
        return month_statistics.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
