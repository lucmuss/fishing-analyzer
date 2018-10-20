# coding: utf-8

import os
import datetime
import csv
import config
import utils


def export_to_mongodb(data_base):
    location = "fish_database.csv"

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, location)

    with open(abs_file_path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

        for row in csv_reader:

            fish_type, date, hour = utils.strip_row(row)

            if len(row) >= 3:

                if fish_type in config.FISH_TYPES:
                    full_date_string = ' '.join([date, hour])

                    date_time = datetime.datetime.strptime(full_date_string, "%d.%m.%Y %H:%M:%S")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    data_base.add_fish(type=fish_type, date=formatted_string, id=None)


from data.model import database_model

export_to_mongodb(database_model)
