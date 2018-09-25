import csv
import datetime
import settings
from container import custom_logger

custom_logger = custom_logger.CustomLogger()
logger = custom_logger.get_logger(__name__)

class FishDatabase:
    __water_temperature = dict()

    __air_temperature = dict()
    __relative_humidity = dict()

    __ground_temperature_5 = dict()
    __ground_temperature_10 = dict()
    __ground_temperature_20 = dict()
    __ground_temperature_50 = dict()
    __ground_temperature_100 = dict()

    __wind_strength = dict()
    __wind_direction = dict()

    __sun_hours = dict()
    __precipitation_amount = dict()

    __fish_catch_values = list()

    __arff_data_list = list()
    __arff_label_list = list()

    __output_line_list = list()

    __added_counter = 0

    def read_air_temperature(self, file_path):

        self.__air_temperature = self.__load_cache('air_temperature', self.__air_temperature)

        if self.__air_temperature:
            return True

        with open(file_path,
                  newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, temperature, humidity, error = row
                station, date, typ, temperature, humidity, error = station.strip(), date.strip(), typ.strip(), temperature.strip(), humidity.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    float_temp = float(temperature)
                    self.__air_temperature[formatted_string] = float_temp

        self.__store_cache('air_temperature', self.__air_temperature)

    def read_relative_humidity(self, file_path):

        self.__relative_humidity = self.__load_cache('relative_humidity', self.__relative_humidity)

        if self.__relative_humidity:
            return True

        with open(file_path,
                  newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, temperature, humidity, error = row
                station, date, typ, temperature, humidity, error = station.strip(), date.strip(), typ.strip(), temperature.strip(), humidity.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    float_humidity = float(humidity)
                    self.__relative_humidity[formatted_string] = float_humidity

        self.__store_cache('relative_humidity', self.__relative_humidity)

    def read_wind_strength(self, file_path):

        self.__wind_strength = self.__load_cache('wind_strength', self.__wind_strength)

        if self.__wind_strength:
            return True

        with open(file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, strength, direction, a, = row
                station, date, typ, strength, direction = station.strip(), date.strip(), typ.strip(), strength.strip(), direction.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    wind_strength = float(strength)
                    self.__wind_strength[formatted_string] = wind_strength

        self.__store_cache('wind_strength', self.__wind_strength)

    def read_wind_direction(self, file_path):

        self.__wind_direction = self.__load_cache('wind_direction', self.__wind_direction)

        if self.__wind_direction:
            return True

        with open(file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, strength, direction, a, = row
                station, date, typ, strength, direction = station.strip(), date.strip(), typ.strip(), strength.strip(), direction.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    wind_direction = float(direction)
                    self.__wind_direction[formatted_string] = wind_direction

        self.__store_cache('wind_direction', self.__wind_direction)

    def read_sun_hours(self, file_path):

        self.__sun_hours = self.__load_cache('sun_hours', self.__sun_hours)

        if self.__sun_hours:
            return True

        with open(file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, sun_minutes, error = row
                station, date, typ, sun_minutes, error = station.strip(), date.strip(), typ.strip(), sun_minutes.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y")
                    sun_minutes = float(sun_minutes)

                    if sun_minutes:
                        sun_minutes = sun_minutes / 60.0

                    if formatted_string in self.__sun_hours:
                        self.__sun_hours[formatted_string] += sun_minutes
                    else:
                        self.__sun_hours[formatted_string] = sun_minutes

        self.__store_cache('sun_hours', self.__sun_hours)

    def read_precipitation_amount(self, file_path):

        self.__precipitation_amount = self.__load_cache('precipitation_amount', self.__precipitation_amount)

        if self.__precipitation_amount:
            return True

        with open(file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, precipitation_amount, a, b, error = row
                station, date, typ, precipitation_amount, error = station.strip(), date.strip(), typ.strip(), precipitation_amount.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y")
                    precipitation_amount = float(precipitation_amount)

                    if formatted_string in self.__precipitation_amount:
                        self.__precipitation_amount[formatted_string] += precipitation_amount
                    else:
                        self.__precipitation_amount[formatted_string] = precipitation_amount

        self.__store_cache('precipitation_amount', self.__precipitation_amount)

    def read_ground_temperature(self, file_path):

        self.__ground_temperature_5 = self.__load_cache('ground_temperature_5', self.__ground_temperature_5)
        self.__ground_temperature_10 = self.__load_cache('ground_temperature_10',
                                                         self.__ground_temperature_10)
        self.__ground_temperature_20 = self.__load_cache('ground_temperature_20',
                                                         self.__ground_temperature_20)
        self.__ground_temperature_50 = self.__load_cache('ground_temperature_50',
                                                         self.__ground_temperature_50)
        self.__ground_temperature_100 = self.__load_cache('ground_temperature_100',
                                                          self.__ground_temperature_100)

        if self.__ground_temperature_5 and self.__ground_temperature_10 and self.__ground_temperature_20 and self.__ground_temperature_50 and self.__ground_temperature_100:
            return True

        with open(file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    ground_temperature_5 = float(temp5)
                    ground_temperature_10 = float(temp10)
                    ground_temperature_20 = float(temp20)
                    ground_temperature_50 = float(temp50)
                    ground_temperature_100 = float(temp100)

                    self.__ground_temperature_5[formatted_string] = ground_temperature_5
                    self.__ground_temperature_10[formatted_string] = ground_temperature_10
                    self.__ground_temperature_20[formatted_string] = ground_temperature_20
                    self.__ground_temperature_50[formatted_string] = ground_temperature_50
                    self.__ground_temperature_100[formatted_string] = ground_temperature_100

        self.__store_cache('ground_temperature_5', self.__ground_temperature_5)
        self.__store_cache('ground_temperature_10', self.__ground_temperature_10)
        self.__store_cache('ground_temperature_20', self.__ground_temperature_20)
        self.__store_cache('ground_temperature_50', self.__ground_temperature_50)
        self.__store_cache('ground_temperature_100', self.__ground_temperature_100)

    def read_raw_data(self, import_file):
        with open(import_file, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                fish_class, date, hour = row
                fish_class, date, hour = fish_class.strip(), date.strip(), hour.strip()

                if len(row) >= 3:
                    full_date_string = date + "-" + hour

                    date_time = datetime.datetime.strptime(full_date_string, "%d.%m.%Y-%H:%M:%S")

                    self.add_fish(fish_class, date_time)
                else:
                    logger.warning("Fish with wrong parameter set was ignored. | Data: {}".format(row))

        logger.info("Fish container was extracted correctly form CSV file. | Filename: {}".format(import_file))

    def add_fish(self, fish_type, date_time):

        date_time_year = date_time.year

        if (fish_type in settings.ALLOWED_FISH_TYPES) and (settings.MINIMAL_YEAR <= date_time_year):
            full_string = date_time.strftime("%d.%m.%Y %H")
            hour_string = date_time.strftime("%H%M")
            datum_string = date_time.strftime("%d.%m.%Y")
            date_string = date_time.strftime("%m%d")

            hour_int = int(hour_string)
            date_int = int(date_string)

            value = (fish_type, datum_string, full_string, hour_int, date_int)

            self.__fish_catch_values.append(value)
            self.__added_counter += 1

            logger.debug(
                "New Fish was added to the container set. | Data: {}".format(value))

            logger.info(
                "New Fish was added to the container set. | Class: {} | Catch Date: {}".format(fish_type,
                                                                                          full_string))
        else:
            logger.warning(
                "Fish with wrong attributes was identified. | Year: {} | Class: {}".format(date_time_year,
                                                                                           fish_type))

    def __get_water_temperature(self, datum_hour_string):
        return self.__water_temperature.get(datum_hour_string, 0.0)

    def __get_air_temperature(self, datum_hour_string):
        return self.__air_temperature.get(datum_hour_string, 0.0)

    def __get_relative_humidity(self, datum_hour_string):
        return self.__relative_humidity.get(datum_hour_string, 0.0)

    def __get_ground_temperature_5(self, datum_hour_string):
        return self.__ground_temperature_5.get(datum_hour_string, 0.0)

    def __get_ground_temperature_10(self, datum_hour_string):
        return self.__ground_temperature_10.get(datum_hour_string, 0.0)

    def __get_ground_temperature_20(self, datum_hour_string):
        return self.__ground_temperature_20.get(datum_hour_string, 0.0)

    def __get_ground_temperature_50(self, datum_hour_string):
        return self.__ground_temperature_50.get(datum_hour_string, 0.0)

    def __get_ground_temperature_100(self, datum_hour_string):
        return self.__ground_temperature_100.get(datum_hour_string, 0.0)

    def __get_wind_strength(self, datum_hour_string):
        return self.__wind_strength.get(datum_hour_string, 0.0)

    def __get_wind_direction(self, datum_hour_string):
        return self.__wind_direction.get(datum_hour_string, 0.0)

    def __get_sun_hours(self, date_string):
        return_value = self.__sun_hours.get(date_string, 0.0)
        string_value = "{0:.1f}".format(return_value)
        float_value = float(string_value)
        return float_value

    def __get_precipitation_amount(self, date_string):
        return_value = self.__precipitation_amount.get(date_string, 0.0)
        string_value = "{0:.1f}".format(return_value)
        float_value = float(string_value)
        return float_value

    def __get_previous_date(self, full_string, days_int):
        current_day = datetime.datetime.strptime(full_string, "%d.%m.%Y")
        previous_day = current_day - datetime.timedelta(days=days_int)
        string_date = previous_day.strftime("%d.%m.%Y")
        return string_date

    def __get_previous_hour_date(self, date_hour_string, days_int):
        current_day = datetime.datetime.strptime(date_hour_string, "%d.%m.%Y %H")
        previous_day = current_day - datetime.timedelta(days=days_int)
        string_date = previous_day.strftime("%d.%m.%Y %H")
        return string_date

    def __get_data_values(self, fish_type, datum_hour_string, datum_string, day_string):
        water_temperature = self.__get_water_temperature(datum_hour_string)
        air_temperature = self.__get_air_temperature(datum_hour_string)
        relative_humidity = self.__get_relative_humidity(datum_hour_string)

        ground_temperature_5 = self.__get_ground_temperature_5(datum_hour_string)
        ground_temperature_10 = self.__get_ground_temperature_10(datum_hour_string)
        ground_temperature_20 = self.__get_ground_temperature_20(datum_hour_string)
        ground_temperature_50 = self.__get_ground_temperature_50(datum_hour_string)
        ground_temperature_100 = self.__get_ground_temperature_100(datum_hour_string)

        wind_strength = self.__get_wind_strength(datum_hour_string)
        wind_direction = self.__get_wind_direction(datum_hour_string)

        sun_hours = self.__get_sun_hours(datum_string)
        precipitation_amount = self.__get_precipitation_amount(datum_string)

        if air_temperature:
            return_list = [
                (day_string + '_wasser_temperatur', str(water_temperature)),
                (day_string + '_luft_temperatur', str(air_temperature)),
                (day_string + '_relative_luft_feuchte', str(relative_humidity)),
                (day_string + '_boden_temperatur_5cm', str(ground_temperature_5)),
                (day_string + '_boden_temperatur_10cm', str(ground_temperature_10)),
                (day_string + '_boden_temperatur_20cm', str(ground_temperature_20)),
                (day_string + '_boden_temperatur_50cm', str(ground_temperature_50)),
                (day_string + '_boden_temperatur_100cm', str(ground_temperature_100)),
                (day_string + '_wind_staerke', str(wind_strength)),
                (day_string + '_wind_richtung', str(wind_direction)),
                (day_string + '_sonnen_stunden', str(sun_hours)),
                (day_string + '_niederschlag_menge', str(precipitation_amount)),
            ]

            logger.debug(
                "Fish container was extracted correctly. | Class: {} Catch Date: {} Data: {}".format(fish_type,
                                                                                                datum_string,
                                                                                                str(
                                                                                                    return_list)))
        else:
            return_list = []

        return return_list

    def __get_class_values(self, fish_type, hour_24_int, date_int):
        return_list = [
            ('datum_monat_tag', str(date_int)),
            ('fangzeit_24_stunden', str(hour_24_int)),
            ('class_label', str(fish_type)),
        ]

        return return_list

    def generate_arff_content(self):
        return_list = list()

        return_list.append("")
        return_list.append("@RELATION AngelDaten")

        for label_item in self.__arff_label_list:

            if label_item == 'class_label':
                return_list.append("@ATTRIBUTE class {Karpfen, Forelle, Brachse, Barbe, Hecht, Aal}")
            else:
                return_list.append("@ATTRIBUTE {} NUMERIC".format(label_item))

        return_list.append("")
        return_list.append("@DATA")

        for data_point in self.__arff_data_list:
            data_string = ','.join(data_point)
            return_list.append(data_string)

        self.__output_line_list = return_list

        logger.info(
            "ARFF File content was correctly built.")

    def process_data_attributes(self):
        counter = 0

        for fish_type, datum_string, datum_hour_string, hour_24_int, date_int in self.__fish_catch_values:

            one_data_point = []

            for previous_day in range(0, settings.MAX_PREVIOUS_DAYS):
                current_date = self.__get_previous_date(datum_string, previous_day)
                current_hour_date = self.__get_previous_hour_date(datum_hour_string, previous_day)

                data_value_tuples = self.__get_data_values(fish_type, current_hour_date,
                                                           current_date, str(previous_day))

                data_points = [value for key, value in data_value_tuples]

                if not counter:
                    day_labels = [key for key, value in data_value_tuples]
                    self.__arff_label_list.extend(day_labels)

                one_data_point.extend(data_points)

            if one_data_point:
                data_value_tuples = self.__get_class_values(fish_type, hour_24_int, date_int)
                data_points = [value for key, value in data_value_tuples]

                if not counter:
                    class_labels = [key for key, value in data_value_tuples]
                    self.__arff_label_list.extend(class_labels)

                one_data_point.extend(data_points)

                self.__arff_data_list.append(one_data_point)

            counter += 1

    #    def get_dataframe(self):
    #        for row in self.__arff_data_list:
    #           pass

    def print_arff_content(self):
        for row in self.__output_line_list:
            print(row)

    def store_arff_file(self):
        with open('output_data_set.arff', 'w') as file:
            for line in self.__output_line_list:
                file.write(line)
                file.write("\n")

        logger.info(
            "ARFF File was correctly stored.")


# Climate Data 2018 Marc
# Fish Database


fish_database = FishDatabase()

fish_database.read_raw_data('rawdata/fish_database.csv')

fish_database.read_water_temperature('weather_data/water_temperature/wassertemperatur_603100044.csv')

fish_database.read_air_temperature(
    'weather_data/relativ_humidity_air_temperature/produkt_tu_stunde_19490101_20171231_00282.txt')

fish_database.read_relative_humidity(
    'weather_data/relativ_humidity_air_temperature/produkt_tu_stunde_19490101_20171231_00282.txt')

fish_database.read_ground_temperature(
    'weather_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt')

fish_database.read_wind_strength('weather_data/wind_strength/produkt_ff_stunde_19490101_20171231_00282.txt')

fish_database.read_wind_direction('weather_data/wind_strength/produkt_ff_stunde_19490101_20171231_00282.txt')

fish_database.read_sun_hours('weather_data/sun_hours/produkt_sd_stunde_19490101_20171231_00282.txt')

fish_database.read_precipitation_amount(
    'weather_data/precipitation_amount/produkt_rr_stunde_19490101_20171231_00282.txt')

fish_database.process_data_attributes()

fish_database.generate_arff_content()

fish_database.print_arff_content()

fish_database.store_arff_file()
