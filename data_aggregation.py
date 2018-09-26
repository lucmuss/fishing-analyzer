import pandas as pd

from dataset.water_temperature import WaterTemperature
from dataset.air_temperature import AirTemperature
from dataset.wind_direction import WindDirection
from dataset.precipitation_amount import PrecipitationAmount
from dataset.relative_humidity import RelativeHumidity
from dataset.sun_hours import SunHours
from dataset.wind_strength import WindStrength
from dataset.ground_temperature import GroundTemperature2
from dataset.ground_temperature import GroundTemperature5
from dataset.ground_temperature import GroundTemperature10
from dataset.ground_temperature import GroundTemperature20
from dataset.ground_temperature import GroundTemperature50
from dataset.ground_temperature import GroundTemperature100

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

ground_temperature_2 = GroundTemperature2()
ground_temperature_2_series = ground_temperature_2.get_series()

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

data_set = {air_temperature.data_name: air_temperature_series,
            water_temperature.data_name: water_temperature_series,
            wind_direction.data_name: wind_direction_series,
            precipitation_amount.data_name: precipitation_amount_series,
            relative_humidity.data_name: relative_humidity_series,
            sun_hours.data_name: sun_hours_series,
            wind_strength.data_name: wind_strength_series,
            ground_temperature_2.data_name: ground_temperature_2_series,
            ground_temperature_5.data_name: ground_temperature_5_series,
            ground_temperature_10.data_name: ground_temperature_10_series,
            ground_temperature_20.data_name: ground_temperature_20_series,
            ground_temperature_50.data_name: ground_temperature_50_series,
            ground_temperature_100.data_name: ground_temperature_100_series}

data_frame = pd.DataFrame(data_set)


def get_year_series(year, series):
    date_start = "{}-01-01 00:00:00".format(year)
    date_end = "{}-12-31 00:00:00".format(year)

    return series[date_start:date_end]


year_serie = get_year_series('2017', water_temperature_series)

x_values = list(year_serie.index.get_values())
y_values = list(year_serie)
