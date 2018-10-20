# coding: utf-8

import pandas
import datetime
import calendar
import config
import pymongo

import utils

from data.fish import CatchMonth
from data.fish import CatchHour
from data.fish import CatchDate
from data.fish import FishType

from data.cache import DataCache

from data.environment import WaterTemperature
from data.environment import AirTemperature
from data.environment import WindDirection
from data.environment import PrecipitationAmount
from data.environment import PrecipitationAmountDay
from data.environment import RelativeHumidity
from data.environment import SunHours
from data.environment import SunMinutes
from data.environment import WindStrength
#from data.environment import GroundTemperature2
from data.environment import GroundTemperature5
from data.environment import GroundTemperature10
from data.environment import GroundTemperature20
from data.environment import GroundTemperature50
from data.environment import GroundTemperature100
from data.environment import RecordDateHour


class FishBaseModel:

    def __init__(self, database_model=None):
        # data attributes form the fish database
        self.catch_date = CatchDate(database_model=database_model)
        self.fish_type = FishType(database_model=database_model)
        self.catch_hour = CatchHour(database_model=database_model)
        self.catch_month = CatchMonth(database_model=database_model)


class EnvironmentBaseModel:

    def __init__(self):
        cache = DataCache()
        # data attributes form the environment data
        self.wind_strength = WindStrength(data_cache=cache)
        self.record_date_hour = RecordDateHour(data_cache=cache)
        self.water_temperature = WaterTemperature(data_cache=cache)
        self.air_temperature = AirTemperature(data_cache=cache)
        self.wind_direction = WindDirection(data_cache=cache)
        self.precipitation_amount = PrecipitationAmount(data_cache=cache)
        self.precipitation_amount_day = PrecipitationAmountDay(data_cache=cache)
        self.relative_humidity = RelativeHumidity(data_cache=cache)
        self.sun_hours = SunHours(data_cache=cache)
        self.sun_minutes = SunMinutes(data_cache=cache)
        #self.ground_temperature_2 = GroundTemperature2(data_cache=cache)
        self.ground_temperature_5 = GroundTemperature5(data_cache=cache)
        self.ground_temperature_10 = GroundTemperature10(data_cache=cache)
        self.ground_temperature_20 = GroundTemperature20(data_cache=cache)
        self.ground_temperature_50 = GroundTemperature50(data_cache=cache)
        self.ground_temperature_100 = GroundTemperature100(data_cache=cache)


class FullBaseModel:
    def __init__(self, environment_model=None, fish_model=None):
        self.environment_model = environment_model
        self.fish_model = fish_model


class DatabaseModel():

    def __init__(self):
        self.__initialize_mongo_db()
        self.__fish_list = list()

    def __del__(self):
        self.mongo_client.close()

    def __initialize_mongo_db(self):

        self.mongo_client = pymongo.MongoClient()
        self.mongo_db = self.mongo_client.get_database(name=config.DATABASE_NAME)

        collection_names = self.mongo_db.collection_names()

        if not config.DATABASE_COLLECTION_NAME in collection_names:
            self.mongo_db.create_collection(config.DATABASE_COLLECTION_NAME)

        self.mongo_collection = self.mongo_db.get_collection(config.DATABASE_COLLECTION_NAME)

    def add_fish(self, type, date, id):

        default_id = id if id else config.DEFAULT_DATASET_ID

        return self._add_fish(type, date, default_id)

    def _add_fish(self, fish_type, catch_date, dataset_id):
        catch_date = datetime.datetime.strptime(catch_date, config.CATCH_DATE_FORMAT)

        return_value = False

        if fish_type in config.FISH_TYPES:

            document = utils.get_database_document(fish_type, catch_date, dataset_id)

            cursor = self.mongo_collection.find(document).limit(1)

            if cursor.count() <= 0:
                self.mongo_collection.insert_one(document)
                return_value = True

        return return_value

    def remove_fish(self, type, date, id):
        default_id = id if id else config.DEFAULT_DATASET_ID

        return self._remove_fish(type, date, default_id)

    def _remove_fish(self, fish_type, catch_date, dataset_id):
        catch_date = datetime.datetime.strptime(catch_date, config.CATCH_DATE_FORMAT)

        return_value = False

        if fish_type in config.FISH_TYPES:

            document = utils.get_database_document(fish_type, catch_date, dataset_id)

            cursor = self.mongo_collection.find(document).limit(1)

            if cursor.count() >= 0:
                self.mongo_collection.delete_one(document)
                return_value = True

        return return_value

    @property
    def fish_list(self):

        if not self.__fish_list:
            cursor = self.mongo_collection.find()

            for document in cursor:
                self.__fish_list.append(document)

        return self.__fish_list


class DataFrameModel():

    def __init__(self, full_base_model):
        self.full_base_model = full_base_model

        is_plotable = lambda series: (series.dtype == 'float64')

        data_set = dict()
        all_attributes = list()
        plotable_attributes = list()

        for attribute, value in self.full_base_model.environment_model.__dict__.items():
            series = value.series

            all_attributes.append(value.attribute_name)

            if is_plotable(series):
                plotable_attributes.append(value.attribute_name)
                series = utils.remove_outliers(series)

            data_set[value.attribute_name] = series

        for attribute, value in self.full_base_model.fish_model.__dict__.items():
            series = value.series

            all_attributes.append(value.attribute_name)

            if is_plotable(series):
                plotable_attributes.append(value.attribute_name)
                series = utils.remove_outliers(series)

            data_set[value.attribute_name] = series

        self.plotable_attributes = plotable_attributes
        self.all_attributes = all_attributes

        self.data_frame = pandas.DataFrame(data_set)


class FishFrameModel():

    def __init__(self, data_frame_model):
        self.data_frame_model = data_frame_model
        self.plotable_attributes = self.data_frame_model.plotable_attributes

        self.data_frame = self.data_frame_model.data_frame.query("fish_type == fish_type")

    def get_fish_frame(self, fish_type):
        fish_data = self.data_frame

        if fish_type in config.FISH_TYPES:
            fish_data = fish_data.query("fish_type == '{}'".format(fish_type))

        return fish_data


class FishStatisticModel():

    def __init__(self, data_frame_model):
        self.data_frame_model = data_frame_model
        self.plotable_attributes = self.data_frame_model.plotable_attributes

        self.month_statistics = self.__process_month_statistics()
        self.data_year_dict = self.__process_year_dict()

    def __process_month_statistics(self):

        return_dict = dict()

        for year in config.YEAR_RANGE:

            for attribute in self.plotable_attributes:
                month_dict = dict()

                for month_index, month_name in config.MONTH_NAME_DICT.items():
                    month_data = self.get_frame_by_month(year, month_index)
                    data_series = month_data[attribute]

                    attribute_mean = data_series.mean()
                    attribute_sum = data_series.sum()

                    month_dict[month_index] = (attribute_mean, attribute_sum)

                return_dict[(year, attribute)] = month_dict

        return return_dict

    def __process_year_dict(self):
        return_dict = dict()

        for year in config.YEAR_RANGE:
            return_dict[year] = self.get_frame_by_year(year)

        return return_dict

    def get_frame_by_year(self, year):
        date_start = "{}-01-01 00:00:00".format(year)
        date_end = "{}-12-31 00:00:00".format(year)

        return self.data_frame_model.data_frame[date_start:date_end]

    def get_frame_by_month(self, year, month):

        year_int = int(year)
        month_int = int(month)

        maximal_month_days = calendar.monthrange(year_int, month_int)[1]

        date_start = "{}-{:02d}-{:02d} 00:00:00".format(year_int, month_int, 1)
        date_end = "{}-{:02d}-{:02d} 00:00:00".format(year_int, month_int, maximal_month_days)

        return self.data_frame_model.data_frame[date_start:date_end]

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

        return self.data_frame_model.data_frame[date_start:date_end]


database_model = DatabaseModel()

fish_base_model = FishBaseModel(database_model=database_model)
environment_base_model = EnvironmentBaseModel()
full_base_model = FullBaseModel(environment_model=environment_base_model, fish_model=fish_base_model)

data_frame_model = DataFrameModel(full_base_model)
fish_frame_model = FishFrameModel(data_frame_model)
fish_statistic_model = FishStatisticModel(data_frame_model)
