import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

from dataset.water_temperature import WaterTemperature
from dataset.air_temperature import AirTemperature
from dataset.wind_direction import WindDirection
from dataset.precipitation_amount import PrecipitationAmount
from dataset.relative_humidity import RelativeHumidity
from dataset.sun_hours import SunHours
from dataset.wind_strength import WindStrength
from dataset.ground_temperature import GroundTemperature5
from dataset.ground_temperature import GroundTemperature10
from dataset.ground_temperature import GroundTemperature20
from dataset.ground_temperature import GroundTemperature50
from dataset.ground_temperature import GroundTemperature100
from dataset.record_date_hour import RecordDateHour

from fishdata.catch_date import CatchDate
from fishdata.fish_type import FishType
from fishdata.catch_hour import CatchHour
from fishdata.catch_month import CatchMonth

from settings import MAXIMAL_SERIES_END_YEAR
from settings import MINIMAL_SERIES_START_YEAR


class FishDataFrame:
    __data_frame = 0
    __std_factor = 3.0
    __data_attribute_names = list()
    __data_year_dict = dict()

    def __init__(self):
        self.__init_data()

    def __init_data(self):
        # data attributes form the fish database
        catch_date = CatchDate()
        catch_date_series = catch_date.get_series()

        fish_type = FishType()
        fish_type_series = fish_type.get_series()

        catch_hour = CatchHour()
        catch_hour_series = catch_hour.get_series()

        catch_month = CatchMonth()
        catch_month_series = catch_month.get_series()

        # data attributes form the environment data
        record_date_hour = RecordDateHour()
        record_date_hour_series = record_date_hour.get_series()

        water_temperature = WaterTemperature()
        water_temperature_series = water_temperature.get_series()

        air_temperature = AirTemperature()
        air_temperature_series = air_temperature.get_series()

        wind_direction = WindDirection()
        wind_direction_series = wind_direction.get_series()

        precipitation_amount = PrecipitationAmount()
        precipitation_amount_series = precipitation_amount.get_series()

        relative_humidity = RelativeHumidity()
        relative_humidity_series = relative_humidity.get_series()

        sun_hours = SunHours()
        sun_hours_series = sun_hours.get_series()

        wind_strength = WindStrength()
        wind_strength_series = wind_strength.get_series()

        ground_temperature_5 = GroundTemperature5()
        ground_temperature_5_series = ground_temperature_5.get_series()

        ground_temperature_10 = GroundTemperature10()
        ground_temperature_10_series = ground_temperature_10.get_series()

        ground_temperature_20 = GroundTemperature20()
        ground_temperature_20_series = ground_temperature_20.get_series()

        ground_temperature_50 = GroundTemperature50()
        ground_temperature_50_series = ground_temperature_50.get_series()

        ground_temperature_100 = GroundTemperature100()
        ground_temperature_100_series = ground_temperature_100.get_series()

        data_set = {catch_date.data_name: catch_date_series,
                    fish_type.data_name: fish_type_series,
                    catch_hour.data_name: catch_hour_series,
                    catch_month.data_name: catch_month_series,
                    record_date_hour.data_name: record_date_hour_series,

                    air_temperature.data_name: self.__remove_outliers(air_temperature_series),
                    water_temperature.data_name: self.__remove_outliers(water_temperature_series),
                    wind_direction.data_name: self.__remove_outliers(wind_direction_series),
                    precipitation_amount.data_name: self.__remove_outliers(precipitation_amount_series),
                    relative_humidity.data_name: self.__remove_outliers(relative_humidity_series),
                    sun_hours.data_name: self.__remove_outliers(sun_hours_series),
                    wind_strength.data_name: self.__remove_outliers(wind_strength_series),
                    ground_temperature_5.data_name: self.__remove_outliers(ground_temperature_5_series),
                    ground_temperature_10.data_name: self.__remove_outliers(ground_temperature_10_series),
                    ground_temperature_20.data_name: self.__remove_outliers(ground_temperature_20_series),
                    ground_temperature_50.data_name: self.__remove_outliers(ground_temperature_50_series),
                    ground_temperature_100.data_name: self.__remove_outliers(ground_temperature_100_series)
                    }

        self.__data_frame = pd.DataFrame(data_set)

        self.__data_attribute_names = self.__get_data_attributes(self.__data_frame)
        self.__data_attribute_names_plot = self.__get_plotable_attributes(self.__data_frame)

    @property
    def plotable_attributes(self):
        return self.__data_attribute_names_plot

    @property
    def data_attributes(self):
        return self.__data_attribute_names

    def __get_data_attributes(self, data_frame):
        return list(data_frame.keys())

    def __get_plotable_attributes(self, data_frame):
        return_list = [name for name in data_frame.columns if (data_frame[name].dtype == 'float64')]
        return return_list

    def get_frame_by_year(self, year):
        date_start = "{}-01-01 00:00:00".format(year)
        date_end = "{}-12-31 00:00:00".format(year)

        return self.__data_frame[date_start:date_end]

    def __remove_outliers(self, panda_series):
        mean_value = panda_series.mean()
        std_value = panda_series.std()
        compare_factor = self.__std_factor * std_value

        bad_index = panda_series[np.abs(panda_series - mean_value) >= compare_factor]
        panda_series = panda_series.drop(index=bad_index.index)

        return panda_series

    def __get_year_list(self):
        date_time_start = datetime.datetime.strptime(MINIMAL_SERIES_START_YEAR, "%Y-%m-%d %H:00:00")
        year_start = date_time_start.strftime("%Y")
        year_start_int = int(year_start)

        date_time_end = datetime.datetime.strptime(MAXIMAL_SERIES_END_YEAR, "%Y-%m-%d %H:00:00")
        year_end = date_time_end.strftime("%Y")
        year_end_int = int(year_end)

        year_range = range(year_start_int, year_end_int + 1)
        year_return_list = [str(year) for year in year_range]

        return year_return_list

    def get_year_dict(self):
        for year in self.__get_year_list():
            self.__data_year_dict[year] = self.get_frame_by_year(year)

        self.__data_year_dict['*'] = self.__data_frame

        return self.__data_year_dict


fish_data = FishDataFrame()

# air_temperature_year_2017 = fish_year_dict['2017']['air_temperature']
# air_temperature_year_2017_filtered = fish_data.remove_outliers(air_temperature_year_2017)

# data_temp_hoch = data_year_2017.query('air_temperature > 28')
# data_temp_hoch.plot.line()

# x_values = list(air_temperature_year_2017_filtered.index.get_values())
# y_values = list(air_temperature_year_2017_filtered)
