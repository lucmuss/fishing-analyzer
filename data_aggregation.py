import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

            air_temperature.data_name: air_temperature_series,
            water_temperature.data_name: water_temperature_series,
            wind_direction.data_name: wind_direction_series,
            precipitation_amount.data_name: precipitation_amount_series,
            relative_humidity.data_name: relative_humidity_series,
            sun_hours.data_name: sun_hours_series,
            wind_strength.data_name: wind_strength_series,
            ground_temperature_5.data_name: ground_temperature_5_series,
            ground_temperature_10.data_name: ground_temperature_10_series,
            ground_temperature_20.data_name: ground_temperature_20_series,
            ground_temperature_50.data_name: ground_temperature_50_series,
            ground_temperature_100.data_name: ground_temperature_100_series,
            record_date_hour.data_name: record_date_hour_series}

data_frame = pd.DataFrame(data_set)


def get_frame_by_year(year, panda_object):
    date_start = "{}-01-01 00:00:00".format(year)
    date_end = "{}-12-31 00:00:00".format(year)

    return panda_object[date_start:date_end]


def remove_outliers(std_factor, panda_object):
    mean_value = panda_object.mean()
    std_value = panda_object.std()
    compare_factor = std_factor * std_value

    bad_index = panda_object[np.abs(panda_object - mean_value) >= compare_factor]
    panda_object = panda_object.drop(index=bad_index.index)

    return panda_object


def print_hist(panda_object):
    data_values = panda_object.get_values()
    plt.hist(data_values)


data_year_2017 = get_frame_by_year('2017', data_frame)
air_temperature_year_2017 = data_year_2017['air_temperature']

air_temperature_year_2017_filterd = remove_outliers(3, air_temperature_year_2017)

# data_temp_hoch = data_year_2017.query('air_temperature > 28')
# data_temp_hoch.plot.line()

x_values = list(air_temperature_year_2017_filterd.index.get_values())
y_values = list(air_temperature_year_2017_filterd)
