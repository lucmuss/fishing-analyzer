from container.water_temperature import WaterTemperature
from container.air_temperature import AirTemperature
import pandas as pd

water_temperature = WaterTemperature()
water_temperature_series = water_temperature.get_series()

air_temperature = AirTemperature()
air_temperature_series = air_temperature.get_series()

data_set = {'air_temperature': air_temperature_series,
            'water_temperature': water_temperature_series}

data_frame = pd.DataFrame(data_set)


def get_year_series(year, series):
    date_start = "{}-01-01 00:00:00".format(year)
    date_end = "{}-12-31 00:00:00".format(year)

    return series[date_start:date_end]


year_serie = get_year_series('2017', water_temperature_series)

x_values = list(year_serie.index.get_values())
y_values = list(year_serie)
