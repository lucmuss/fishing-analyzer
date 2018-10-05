import flask
import dash

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
app.config.supress_callback_exceptions = True