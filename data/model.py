# coding: utf-8

import pandas
import datetime
import calendar
import config
import pymongo

import utils

from data.fish.catch_month import CatchMonth
from data.fish.catch_hour import CatchHour
from data.fish.catch_date import CatchDate
from data.fish.fish_type import FishType

from data.cache import DataCache
from data.cache import DatabaseDataCache

from data.environment.water_temperature import WaterTemperature
from data.environment.air_temperature import AirTemperature
from data.environment.wind_direction import WindDirection
from data.environment.precipitation_amount import PrecipitationAmount
from data.environment.precipitation_amount_day import PrecipitationAmountDay
from data.environment.relative_humidity import RelativeHumidity
from data.environment.sun_minutes_day import SunMinutesDay
from data.environment.sun_minutes import SunMinutes
from data.environment.wind_strength import WindStrength
from data.environment.ground_temperature import GroundTemperature5
from data.environment.ground_temperature import GroundTemperature10
from data.environment.ground_temperature import GroundTemperature20
from data.environment.ground_temperature import GroundTemperature50
from data.environment.ground_temperature import GroundTemperature100
from data.environment.record_date_hour import RecordDateHour


class FishBaseModel:

    def __init__(self, database_model=None):
        # data attributes form the fish database
        self.catch_date = CatchDate(database_model=database_model)
        self.fish_type = FishType(database_model=database_model)
        self.catch_hour = CatchHour(database_model=database_model)
        self.catch_month = CatchMonth(database_model=database_model)


class EnvironmentBaseModel:

    def __init__(self, data_cache):
        # data attributes form the environment data
        self.wind_strength = WindStrength(data_cache=data_cache)
        self.record_date_hour = RecordDateHour(data_cache=data_cache)
        self.water_temperature = WaterTemperature(data_cache=data_cache)
        self.air_temperature = AirTemperature(data_cache=data_cache)
        self.wind_direction = WindDirection(data_cache=data_cache)
        self.precipitation_amount = PrecipitationAmount(data_cache=data_cache)
        self.precipitation_amount_day = PrecipitationAmountDay(data_cache=data_cache)
        self.relative_humidity = RelativeHumidity(data_cache=data_cache)
        self.sun_hours = SunMinutesDay(data_cache=data_cache)
        self.sun_minutes = SunMinutes(data_cache=data_cache)
        self.ground_temperature_5 = GroundTemperature5(data_cache=data_cache)
        self.ground_temperature_10 = GroundTemperature10(data_cache=data_cache)
        self.ground_temperature_20 = GroundTemperature20(data_cache=data_cache)
        self.ground_temperature_50 = GroundTemperature50(data_cache=data_cache)
        self.ground_temperature_100 = GroundTemperature100(data_cache=data_cache)


class FullBaseModel:
    def __init__(self, environment_model=None, fish_model=None):
        self.environment_model = environment_model
        self.fish_model = fish_model


class DatabaseModel:

    def __init__(self):
        self.__initialize_mongo_db()
        self.__fish_list = list()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mongo_client.close()

    def __initialize_mongo_db(self):

        self.mongo_client = pymongo.MongoClient()
        self.mongo_db = self.mongo_client.get_database(name=config.DATABASE_NAME)

        collection_names = self.mongo_db.collection_names()

        if config.DATABASE_FISH_COLLECTION_NAME not in collection_names:
            self.mongo_db.create_collection(config.DATABASE_FISH_COLLECTION_NAME)

        self.mongo_collection = self.mongo_db.get_collection(config.DATABASE_FISH_COLLECTION_NAME)

    def add_fish(self, fish_type, catch_date, fisher_id, river_id):

        fisher_id = fisher_id if fisher_id else config.DEFAULT_FISHER_ID
        river_id = river_id if river_id else config.DEFAULT_RIVER_ID

        return self._add_fish(fish_type, catch_date, fisher_id, river_id)

    def _add_fish(self, fish_type, catch_date, fisher_id, river_id):
        catch_date = datetime.datetime.strptime(catch_date, config.CATCH_DATE_FORMAT)

        return_value = False

        if fish_type in config.FISH_TYPES:

            document = utils.get_database_document(fish_type, catch_date, fisher_id, river_id)

            cursor = self.mongo_collection.find(document).limit(1)

            if cursor.count() <= 0:
                self.mongo_collection.insert_one(document)
                return_value = True

        return return_value

    def remove_fish(self, fish_type, catch_date, fisher_id, river_id):
        fisher_id = fisher_id if fisher_id else config.DEFAULT_FISHER_ID
        river_id = river_id if river_id else config.DEFAULT_RIVER_ID

        return self._remove_fish(fish_type, catch_date, fisher_id, river_id)

    def _remove_fish(self, fish_type, catch_date, fisher_id, river_id):
        catch_date = datetime.datetime.strptime(catch_date, config.CATCH_DATE_FORMAT)

        return_value = False

        if fish_type in config.FISH_TYPES:

            document = utils.get_database_document(fish_type, catch_date, fisher_id, river_id)

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


class DataFrameModel:

    def __init__(self, full_base_model):
        self.full_base_model = full_base_model

        data_set = dict()

        plotable_attributes = set()
        environment_attributes = set()
        fish_attributes = set()

        for attribute, value in self.full_base_model.environment_model.__dict__.items():
            series = value.series

            environment_attributes.add(attribute)

            if utils.is_plotable(series):
                plotable_attributes.add(value.attribute_name)
                series = utils.remove_outliers(series)

            data_set[value.attribute_name] = series

        for attribute, value in self.full_base_model.fish_model.__dict__.items():
            series = value.series

            fish_attributes.add(value.attribute_name)

            if utils.is_plotable(series):
                plotable_attributes.add(value.attribute_name)
                series = utils.remove_outliers(series)

            data_set[value.attribute_name] = series

        self.plotable_attributes = plotable_attributes
        self.environment_attributes = environment_attributes
        self.fish_attributes = fish_attributes

        config.ATTRIBUTE_COLOR_DICT = config.get_color_dict(plotable_attributes)

        self.data_frame = pandas.DataFrame(data_set)


class FishFrameModel:

    def __init__(self, data_frame_model):
        self.data_frame_model = data_frame_model
        self.plotable_attributes = self.data_frame_model.plotable_attributes
        self.environment_attributes = self.data_frame_model.environment_attributes
        self.fish_attributes = self.data_frame_model.fish_attributes

        self.data_frame = self.data_frame_model.data_frame.query("fish_type == fish_type")

    def get_fish_frame(self, fish_type):
        fish_data = self.data_frame

        if fish_type in config.FISH_TYPES:
            fish_data = fish_data.query("fish_type == '{}'".format(fish_type))

        return fish_data


class StatisticModel:

    def __init__(self, data_frame_model):
        self.data_frame_model = data_frame_model
        self.plotable_attributes = self.data_frame_model.plotable_attributes
        self.environment_attributes = self.data_frame_model.environment_attributes
        self.fish_attributes = self.data_frame_model.fish_attributes

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

                    mean = data_series.mean()
                    sum = data_series.sum()
                    max = data_series.max()
                    min = data_series.min()

                    month_dict[month_index] = {'mean': mean,
                                               'sum': sum,
                                               'min': min,
                                               'max': max}

                return_dict[(year, attribute)] = month_dict

        return return_dict

    def __process_year_dict(self):
        return_dict = {year: self.get_frame_by_year(year)
                       for year in config.YEAR_RANGE}

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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ModelFactory(metaclass=Singleton):

    def __init__(self):
        self._database_model = None
        self._database_data_cache = None
        self._fish_base_model = None
        self._environment_base_model = None
        self._full_base_model = None
        self._data_frame_model = None
        self._fish_frame_model = None
        self._statistic_model = None

    @property
    def database_model(self):
        if not self._database_model:
            self._database_model = DatabaseModel()

        return self._database_model

    @property
    def database_data_cache(self):
        if not self._database_data_cache:
            self._database_data_cache = DatabaseDataCache(database_model=self.database_model)

        return self._database_data_cache

    @property
    def fish_base_model(self):
        if not self._fish_base_model:
            self._fish_base_model = FishBaseModel(database_model=self.database_model)

        return self._fish_base_model

    @property
    def environment_base_model(self):
        if not self._environment_base_model:
            self._environment_base_model = EnvironmentBaseModel(data_cache=self.database_data_cache)

        return self._environment_base_model

    @property
    def full_base_model(self):
        if not self._full_base_model:
            self._full_base_model = FullBaseModel(environment_model=self.environment_base_model,
                                                  fish_model=self.fish_base_model)

        return self._full_base_model

    @property
    def data_frame_model(self):
        if not self._data_frame_model:
            self._data_frame_model = DataFrameModel(self.full_base_model)

        return self._data_frame_model

    @property
    def fish_frame_model(self):
        if not self._fish_frame_model:
            self._fish_frame_model = FishFrameModel(self.data_frame_model)

        return self._fish_frame_model

    @property
    def statistic_model(self):
        if not self._statistic_model:
            self._statistic_model = StatisticModel(self.data_frame_model)

        return self._statistic_model


if __name__ == '__main__':
    model_factory = ModelFactory()
    statistic_model = model_factory.statistic_model

    model_factory_second = ModelFactory()
    statistic_model = model_factory_second.statistic_model
