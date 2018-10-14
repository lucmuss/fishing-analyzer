import pandas
import config

class CatchDate:
    attribute_name = 'fish_catch_date'

    __data_dict = dict()

    def __init__(self, fish_list):
        self.__read(fish_list)

    @property
    def series(self):
        data_values = list(self.__data_dict.values())
        index_values = list(self.__data_dict.keys())
        series = pandas.Series(data_values, index=index_values, name=self.attribute_name)
        series = series.sort_index()

        reduced_series = series[config.MINIMAL_SERIES_START_YEAR:config.MAXIMAL_SERIES_END_YEAR]
        return reduced_series


    def __read(self, fish_list):
        for document in fish_list:
            catch_date = document['catch_date']

            formatted_string = catch_date.strftime(config.CATCH_DATE_FORMAT)
            catch_date = catch_date.strftime("%Y-%m-%d")

            self.__data_dict[formatted_string] = catch_date