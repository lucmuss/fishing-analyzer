# coding: utf-8

import flask
import dash
import os
from apps import insert

server = flask.Flask(__name__)
server.config.from_object(__name__)
server.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app = dash.Dash(__name__, server=server)
app.config['suppress_callback_exceptions'] = True


@server.route('/apps/insert', methods=['GET', 'POST'])
def insert_fish():
    insert_form = insert.InsertForm(flask.request.form)

    if insert_form.validate():
        insert.store_form(insert_form)
        flask.flash('Fisch wurde gespeichert')

    return flask.render_template('insert.html', form=insert_form)
