# coding: utf-8

import flask
import dash

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server)
app.config['suppress_callback_exceptions'] = True


# TODO
@server.route('/fish/list', methods=['GET'])
def list_fishes():
    return ''
