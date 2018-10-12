import pandas
import numpy
import datetime
import calendar
import config
import pymongo

from data.environment.water_temperature import WaterTemperature
from data.environment.air_temperature import AirTemperature
from data.environment.wind_direction import WindDirection
from data.environment.precipitation_amount import PrecipitationAmount
from data.environment.relative_humidity import RelativeHumidity
from data.environment.sun_hours import SunHours
from data.environment.wind_strength import WindStrength
from data.environment.ground_temperature import GroundTemperature5
from data.environment.ground_temperature import GroundTemperature10
from data.environment.ground_temperature import GroundTemperature20
from data.environment.ground_temperature import GroundTemperature50
from data.environment.ground_temperature import GroundTemperature100
from data.environment.record_date_hour import RecordDateHour

from data.fish.catch_date import CatchDate
from data.fish.fish_type import FishType
from data.fish.catch_hour import CatchHour
from data.fish.catch_month import CatchMonth


def remove_outliers(panda_series):
    mean_value = panda_series.mean()
    std_value = panda_series.std()
    compare_factor = config.STANDARD_DEVIATION_FACTOR * std_value

    bad_index = panda_series[numpy.abs(panda_series - mean_value) >= compare_factor]
    panda_series = panda_series.drop(index=bad_index.index)

    return panda_series


def series_to_graph(panda_series):
    x_values = list(panda_series.index.get_values())
    y_values = list(panda_series.get_values())

    return x_values, y_values


class BaseModel:

    def __init__(self):
        # data attributes form the fish database
        self.catch_date = CatchDate()
        self.fish_type = FishType()
        self.catch_hour = CatchHour()
        self.catch_month = CatchMonth()
        self.record_date_hour = RecordDateHour()

        # data attributes form the environment data
        self.water_temperature = WaterTemperature()
        self.air_temperature = AirTemperature()
        self.wind_direction = WindDirection()
        self.precipitation_amount = PrecipitationAmount()
        self.relative_humidity = RelativeHumidity()
        self.sun_hours = SunHours()
        self.wind_strength = WindStrength()
        self.ground_temperature_5 = GroundTemperature5()
        self.ground_temperature_10 = GroundTemperature10()
        self.ground_temperature_20 = GroundTemperature20()
        self.ground_temperature_50 = GroundTemperature50()
        self.ground_temperature_100 = GroundTemperature100()


class DataFrameModel(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)

        is_plotable = lambda series: (series.dtype == 'float64')

        data_set = dict()
        all_attributes = list()
        plotable_attributes = list()

        for attribute, value in self.__dict__.items():
            series = value.series

            all_attributes.append(value.attribute_name)

            if is_plotable(series):
                plotable_attributes.append(value.attribute_name)
                series = remove_outliers(series)

            data_set[value.attribute_name] = series

        self.plotable_attributes = plotable_attributes
        self.all_attributes = all_attributes

        self.data_frame = pandas.DataFrame(data_set)


class FishFrameModel(DataFrameModel):

    def __init__(self):
        DataFrameModel.__init__(self)

        self.data_frame = self.data_frame.query("fish_type == fish_type")

        self.__initialize_mongo_db()

    def __del__(self):
        self.mongo_client.close()

    def __initialize_mongo_db(self):

        self.mongo_client = pymongo.MongoClient()
        self.mongo_db = self.mongo_client.get_database(name=config.DATABASE_NAME)

        collection_names = self.mongo_db.collection_names()

        if not config.DATABASE_COLLECTION_NAME in collection_names:
            self.mongo_db.create_collection(config.DATABASE_COLLECTION_NAME)

        self.mongo_collection = self.mongo_db.get_collection(config.DATABASE_COLLECTION_NAME)

    def get_fish_frame(self, fish_type):
        fish_data = self.data_frame

        if fish_type in config.ALLOWED_FISH_TYPES:
            fish_data = fish_data.query("fish_type == '{}'".format(fish_type))

        return fish_data

    def add_fish(self, fish_type, catch_date):
        catch_date = datetime.datetime.strptime(catch_date, config.CATCH_DATE_FORMAT)

        return_value = False

        if fish_type in config.ALLOWED_FISH_TYPES:

            document = config.get_database_document(fish_type, catch_date)

            cursor = self.mongo_collection.find(document).limit(1)

            if cursor.count() <= 0:
                self.mongo_collection.insert_one(document)
                return_value = True

        return return_value

    def remove_fish(self, fish_type, catch_date):
        catch_date = datetime.datetime.strptime(catch_date, config.CATCH_DATE_FORMAT)

        return_value = False

        if fish_type in config.ALLOWED_FISH_TYPES:

            document = config.get_database_document(fish_type, catch_date)

            cursor = self.mongo_collection.find(document).limit(1)

            if cursor.count() >= 0:
                self.mongo_collection.delete_one(document)
                return_value = True

        return return_value


class FishStatisticModel(DataFrameModel):

    def __init__(self):
        DataFrameModel.__init__(self)

        self.month_statistics = self.__process_month_statistics()
        self.data_year_dict = self.__process_year_dict()

    def __process_month_statistics(self):

        return_dict = dict()

        for year in config.YEAR_LIST:

            for attribute in self.plotable_attributes:
                month_dict = dict()

                for month_index, month_name in config.MONTH_DICT.items():
                    month_data = self.get_frame_by_month(year, month_index)
                    data_series = month_data[attribute]

                    attribute_mean = data_series.mean()
                    attribute_sum = data_series.sum()

                    month_dict[month_index] = (attribute_mean, attribute_sum)

                return_dict[(year, attribute)] = month_dict

        return return_dict

    def __process_year_dict(self):
        return_dict = dict()

        for year in config.YEAR_LIST:
            return_dict[year] = self.get_frame_by_year(year)

        return return_dict

    def get_frame_by_year(self, year):
        date_start = "{}-01-01 00:00:00".format(year)
        date_end = "{}-12-31 00:00:00".format(year)

        return self.data_frame[date_start:date_end]

    def get_frame_by_month(self, year, month):

        year_int = int(year)
        month_int = int(month)

        maximal_month_days = calendar.monthrange(year_int, month_int)[1]

        date_start = "{}-{:02d}-{:02d} 00:00:00".format(year_int, month_int, 1)
        date_end = "{}-{:02d}-{:02d} 00:00:00".format(year_int, month_int, maximal_month_days)

        return self.data_frame[date_start:date_end]

    def get_frame_by_day(self, year, month, day):

        year_int = int(year)
        month_int = int(month)
        day_int = int(day)

        maximal_month_days = calendar.monthrange(year_int, month_int)[1]

        if day_int > maximal_month_days:
            month_int += 1
            day_int = 1

        date_start = "{}-{:02d}-{:02d} 00:00:00".format(year_int, month_int, day_int)
        date_end = "{}-{:02d}-{:02d} 23:00:00".format(year_int, month_int, day_int)

        return self.data_frame[date_start:date_end]


# fdf = DataFrameModel()
ffm = FishFrameModel()
# fsm = FishStatisticModel()

# df = fish_data.get_data_frame()
# air_temperature_year_2017 = fish_year_dict['2017']['air_temperature']
# air_temperature_year_2017_filtered = fish.remove_outliers(air_temperature_year_2017)

# data_temp_hoch = data_year_2017.query('air_temperature > 28')
# data_temp_hoch.plot.line()

# x_values = list(air_temperature_year_2017_filtered.index.get_values())
# y_values = list(air_temperature_year_2017_filtered)
