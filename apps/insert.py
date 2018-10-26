# coding: utf-8

import datetime

import wtforms
import wtforms_components

import config
from data.model import DatabaseModel


class InsertForm(wtforms.Form):
    fish_type = wtforms.SelectField(label='Fisch Art:',
                                    choices=[(fish_type, fish_type) for fish_type in config.FISH_TYPES],
                                    validators=[wtforms.validators.required()])

    fisher_id = wtforms.SelectField(label='Quelle:', choices=[(fisher_type, fisher_type) for fisher_type in
                                                              config.FISHER_IDS],
                                    validators=[wtforms.validators.required()])

    river_id = wtforms.SelectField(label='Fluss:',
                                   choices=[(river_type, river_type) for river_type in config.RIVER_IDS],
                                   validators=[wtforms.validators.required()])

    catch_date = wtforms_components.DateTimeField(label='Fang Datum:',
                                                  validators=[wtforms_components.validators.DateRange(
                                                      min=datetime.datetime(2000, 1, 1),
                                                      max=datetime.datetime(2020, 10, 10)
                                                  )]
                                                  )

    submit = wtforms.SubmitField(label='Abspeichern')


def store_form(insert_form):
    fish_type = insert_form.fish_type.data
    fisher_id = insert_form.fisher_id.data
    river_id = insert_form.river_id.data
    catch_date = insert_form.catch_date.data

    full_date_string = catch_date

    date_time = datetime.datetime.strptime(full_date_string, "%d.%m.%Y %H:%M:%S")
    formatted_date = date_time.strftime(config.CATCH_DATE_FORMAT)

    catch_date = formatted_date

    db_model = DatabaseModel()
    correct_store = db_model.add_fish(fish_type=fish_type,
                                      fisher_id=fisher_id,
                                      river_id=river_id,
                                      catch_date=catch_date)

    return correct_store
