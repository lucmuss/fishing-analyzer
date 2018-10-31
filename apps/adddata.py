# coding: utf-8

import datetime

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import config
from mainapp import app
from data.model import ModelFactory

model_factory = ModelFactory()
data_base_model = model_factory.database_model


def generate_fish_type_options():
    return_list = list()

    for fish_type in config.FISH_TYPES:
        return_list.append({'label': fish_type, 'value': fish_type})

    return return_list


def generate_river_id_options():
    return_list = list()

    for river_id in config.RIVER_IDS:
        return_list.append({'label': river_id, 'value': river_id})

    return return_list


def generate_fisher_id_options():
    return_list = list()

    for fisher in config.FISHER_IDS:
        return_list.append({'label': fisher, 'value': fisher})

    return return_list


fish_type_options = generate_fish_type_options()
default_fish_type = config.DEFAULT_FISH_TYPE

river_id_options = generate_river_id_options()
default_river_id = config.DEFAULT_RIVER_ID

fisher_id_options = generate_fisher_id_options()
default_fisher_id = config.DEFAULT_FISHER_ID

default_catch_date = config.DEFAULT_CATCH_DATE

default_catch_hour = config.DEFAULT_CATCH_HOUR

layout = html.Div(children=[

    html.Div(id='add_fish_output_message'),

    html.Form(children=[

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-4', children=[
            html.Label('Fish Type'),
            dcc.Dropdown(
                id='add_fish_fish_type',
                options=fish_type_options,
                value=default_fish_type
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-4', children=[
            html.Label('Fisher'),
            dcc.Dropdown(
                id='add_fish_fisher_id',
                options=fisher_id_options,
                value=default_fisher_id
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-4', children=[
            html.Label('River'),
            dcc.Dropdown(
                id='add_fish_river_id',
                options=river_id_options,
                value=default_river_id
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-4', children=[
            html.Label('Catch Date'),
            dcc.Input(
                id='add_fish_catch_date',
                type='date',
                value=default_catch_date,
                className='form-control',
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-4', children=[
            html.Label('Catch Hour'),
            dcc.Input(
                id='add_fish_catch_hour',
                type='time',
                value=default_catch_hour,
                className='form-control',
            ),
        ]),

        html.Div(className='form-group float-left col-xs-3 col-sm-6 col-md-4 col-lg-4', children=[
            html.Label('Store'),
            html.Button(className='form-control btn btn-success',
                        id='add_fish_submit_button',
                        n_clicks=0,
                        children='Store Data')
        ]),

    ]),

])


@app.callback(
    Output('add_fish_output_message', 'children'),
    [Input('add_fish_submit_button', 'n_clicks')],
    [State('add_fish_fish_type', 'value'),
     State('add_fish_river_id', 'value'),
     State('add_fish_fisher_id', 'value'),
     State('add_fish_catch_date', 'value'),
     State('add_fish_catch_hour', 'value')])
def update_data_graph(n_clicks, fish_type, river_id, fisher_id, catch_date, catch_hour):
    return_message = ""

    if n_clicks and fish_type and river_id and fisher_id and catch_date and catch_hour:

        full_date_string = ' '.join([catch_date, catch_hour])

        date_time = datetime.datetime.strptime(full_date_string, "%Y-%m-%d %H:%M")
        formatted_date = date_time.strftime(config.CATCH_DATE_FORMAT)

        correct_store = data_base_model.add_fish(fish_type=fish_type,
                                                 fisher_id=fisher_id,
                                                 river_id=river_id,
                                                 catch_date=formatted_date)

        if correct_store:
            return_message = "Fish was correctly added to database"
        else:
            return_message = "Fish was not correctly added to database"

    return return_message
