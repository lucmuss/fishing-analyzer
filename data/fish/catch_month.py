import csv
import datetime
import pandas
import config
import os


class CatchMonth:
    location = 'fish_database.csv'
    attribute_name = 'fish_catch_month'

    __data_dict = dict()
    __fish_catch_values = list()

    def __init__(self):
        self.__init_data()

    def __init_data(self):

        if self.__data_dict:
            return True

        self.__read()

    @property
    def series(self):
        data_values = list(self.__data_dict.values())
        index_values = list(self.__data_dict.keys())
        series = pandas.Series(data_values, index=index_values, name=self.attribute_name)
        series = series.sort_index()

        reduced_series = series[config.MINIMAL_SERIES_START_YEAR:config.MAXIMAL_SERIES_END_YEAR]
        return reduced_series

    def __read(self):
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, self.location)

        with open(abs_file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                fish_type, date, hour = row
                fish_type, date, hour = fish_type.strip(), date.strip(), hour.strip()

                if len(row) >= 3:
                    full_date_string = date + "-" + hour

                    date_time = datetime.datetime.strptime(full_date_string, "%d.%m.%Y-%H:%M:%S")

                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)
                    catch_month = date_time.strftime("%m")

                    self.__data_dict[formatted_string] = catch_month
