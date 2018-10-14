import flask
import dash

from dash.dependencies import Input, Output

from apps.navigation import header

from apps.visualisation import environmental_data
from apps.visualisation import month_statistics


server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, url_base_pathname='/visualisation/')
app.config['suppress_callback_exceptions'] = True

app.layout = header.layout


@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/visualisation/apps/environmental_data':
        return environmental_data.layout
    elif pathname == '/visualisation/apps/month_statistics':
        return month_statistics.layout
    else:
        return ""
    # elif pathname == '/visualisation/apps/month_statistics':
    # return month_statistics.layout


# TODO
@server.route('/fish/list', methods=['GET'])
def list_fishes():
    return [1]


if __name__ == '__main__':
    app.run_server(debug=True)
