import csv
import datetime


class FangBuch:
    wasser_temp = dict()

    luft_temp = dict()
    relative_feuchte = dict()

    boden_temp_5 = dict()
    boden_temp_10 = dict()
    boden_temp_20 = dict()
    boden_temp_50 = dict()
    boden_temp_100 = dict()

    wind_staerke = dict()
    wind_richtung = dict()

    sonnen_stunden = dict()
    niederschlag_menge = dict()

    fish_catch_values = list()

    arff_data_values = list()
    arff_label_values = list()

    output_line_list = list()

    MAX_PREVIOUS_DAYS = 3

    # fertig
    def read_wasser_temp(self, file_path):
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

            for row in csv_reader:
                if len(row) >= 3 and row[2] == "Rohdaten":
                    datum, temp, typ = row
                    date_time = datetime.datetime.strptime(datum, "%Y-%m-%d %H:%M")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    replaced_temp = temp.replace(',', '.')
                    if not replaced_temp:
                        replaced_temp = "0.0"
                    float_temp = float(replaced_temp)

                    self.wasser_temp[formatted_string] = float_temp
                    d = 0

    # fertig
    def read_luft_temp_luft_feuchte(self, file_path):
        with open(file_path,
                  newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, datum, typ, temp, feuchte, error = row
                station, datum, typ, temp, feuchte, error = station.strip(), datum.strip(), typ.strip(), temp.strip(), feuchte.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(datum, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    float_feuchte = float(feuchte)
                    self.relative_feuchte[formatted_string] = float_feuchte

                    float_temp = float(temp)
                    self.luft_temp[formatted_string] = float_temp

    # fertig
    def read_boden_temp(self, file_path):
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, datum, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, datum, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), datum.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(datum, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    boden_temp_5 = float(temp5)
                    boden_temp_10 = float(temp10)
                    boden_temp_20 = float(temp20)
                    boden_temp_50 = float(temp50)
                    boden_temp_100 = float(temp100)

                    self.boden_temp_5[formatted_string] = boden_temp_5
                    self.boden_temp_10[formatted_string] = boden_temp_10
                    self.boden_temp_20[formatted_string] = boden_temp_20
                    self.boden_temp_50[formatted_string] = boden_temp_50
                    self.boden_temp_100[formatted_string] = boden_temp_100

    # fertig
    def read_wind(self, file_path):
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, datum, typ, strongness, richtung, a, = row
                station, datum, typ, strongness, richtung = station.strip(), datum.strip(), typ.strip(), strongness.strip(), richtung.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(datum, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y %H")

                    staerke_temp = float(strongness)
                    self.wind_staerke[formatted_string] = staerke_temp

                    richtung_temp = float(richtung)
                    self.wind_richtung[formatted_string] = richtung_temp

    # fertig
    def read_sonnenstunden(self, file_path):
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, datum, typ, sonnenminuten, error = row
                station, datum, typ, sonnenminuten, error = station.strip(), datum.strip(), typ.strip(), sonnenminuten.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(datum, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y")
                    sonnen_temp = float(sonnenminuten)

                    if sonnen_temp:
                        sonnen_temp = sonnen_temp / 60.0

                    if formatted_string in self.sonnen_stunden:
                        self.sonnen_stunden[formatted_string] += sonnen_temp
                    else:
                        self.sonnen_stunden[formatted_string] = sonnen_temp

    # fertig
    def read_niederschlag(self, file_path):
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, datum, typ, niederschlag, a, b, error = row
                station, datum, typ, niederschlag, error = station.strip(), datum.strip(), typ.strip(), niederschlag.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(datum, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%d.%m.%Y")
                    niederschlag_temp = float(niederschlag)

                    if formatted_string in self.niederschlag_menge:
                        self.niederschlag_menge[formatted_string] += niederschlag_temp
                    else:
                        self.niederschlag_menge[formatted_string] = niederschlag_temp

    # fertig
    def read_input_data(self, import_file):
        with open(import_file, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

            for row in csv_reader:

                klasse, datum, uhrzeit = row
                klasse, datum, uhrzeit = klasse.strip(), datum.strip(), uhrzeit.strip()

                if len(row) >= 3:
                    full_date_string = datum + "-" + uhrzeit

                    date_time = datetime.datetime.strptime(full_date_string, "%d.%m.%Y-%H:%M:%S")

                    full_string = date_time.strftime("%d.%m.%Y %H")
                    hour_string = date_time.strftime("%H%M")
                    datum_string = date_time.strftime("%d.%m.%Y")
                    date_string = date_time.strftime("%m%d")

                    hour_int = int(hour_string)
                    date_int = int(date_string)

                    value = (klasse, datum_string, full_string, hour_int, date_int)

                    self.fish_catch_values.append(value)

    def get_wasser_temp(self, full_string):
        if full_string in self.wasser_temp:
            wasser_temp = self.wasser_temp[full_string]
        else:
            wasser_temp = 0.0
        return wasser_temp

    def get_luft_temp(self, full_string):
        if full_string in self.luft_temp:
            luft_temp = self.luft_temp[full_string]
        else:
            luft_temp = 0.0
        return luft_temp

    def get_relative_feuchte(self, full_string):
        if full_string in self.relative_feuchte:
            relative_feuchte = self.relative_feuchte[full_string]
        else:
            relative_feuchte = 0.0
        return relative_feuchte

    def get_boden_temp_5(self, full_string):
        if full_string in self.boden_temp_5:
            boden_temp = self.boden_temp_5[full_string]
        else:
            boden_temp = 0.0
        return boden_temp

    def get_boden_temp_10(self, full_string):
        if full_string in self.boden_temp_10:
            boden_temp = self.boden_temp_10[full_string]
        else:
            boden_temp = 0.0
        return boden_temp

    def get_boden_temp_20(self, full_string):
        if full_string in self.boden_temp_20:
            boden_temp = self.boden_temp_20[full_string]
        else:
            boden_temp = 0.0
        return boden_temp

    def get_boden_temp_50(self, full_string):
        if full_string in self.boden_temp_50:
            boden_temp = self.boden_temp_50[full_string]
        else:
            boden_temp = 0.0
        return boden_temp

    def get_boden_temp_100(self, full_string):
        if full_string in self.boden_temp_100:
            boden_temp = self.boden_temp_100[full_string]
        else:
            boden_temp = 0.0
        return boden_temp

    def get_wind_staerke(self, full_string):
        if full_string in self.wind_staerke:
            wind_staerke = self.wind_staerke[full_string]
        else:
            wind_staerke = 0.0
        return wind_staerke

    def get_wind_richtung(self, full_string):
        if full_string in self.wind_richtung:
            wind_richtung = self.wind_richtung[full_string]
        else:
            wind_richtung = 0.0
        return wind_richtung

    def get_sonnen_stunden(self, date_string):
        if date_string in self.sonnen_stunden:
            sonnen_stunden = self.sonnen_stunden[date_string]
        else:
            sonnen_stunden = 0.0
        return self.format_float(sonnen_stunden)

    def get_niederschlag_menge(self, date_string):
        if date_string in self.niederschlag_menge:
            niederschlag_menge = self.niederschlag_menge[date_string]
        else:
            niederschlag_menge = 0.0
        return self.format_float(niederschlag_menge)

    def get_previous_date(self, full_string, days_int):
        aktueller_tag = datetime.datetime.strptime(full_string, "%d.%m.%Y")
        vorheriger_tag = aktueller_tag - datetime.timedelta(days=days_int)
        string_date = vorheriger_tag.strftime("%d.%m.%Y")
        return string_date

    def get_previous_hour_date(self, date_hour_string, days_int):
        aktueller_tag = datetime.datetime.strptime(date_hour_string, "%d.%m.%Y %H")
        vorheriger_tag = aktueller_tag - datetime.timedelta(days=days_int)
        string_date = vorheriger_tag.strftime("%d.%m.%Y %H")
        return string_date

    def format_float(self, value):
        return "{0:.1f}".format(round(value, 2))

    def get_full_tuple_values(self, datum_hour_string, datum_string, day_string):
        wasser_temp = self.get_wasser_temp(datum_hour_string)
        luft_temp = self.get_luft_temp(datum_hour_string)
        relative_feuchte = self.get_relative_feuchte(datum_hour_string)

        boden_temp_5 = self.get_boden_temp_5(datum_hour_string)
        boden_temp_10 = self.get_boden_temp_10(datum_hour_string)
        boden_temp_20 = self.get_boden_temp_20(datum_hour_string)
        boden_temp_50 = self.get_boden_temp_50(datum_hour_string)
        boden_temp_100 = self.get_boden_temp_100(datum_hour_string)

        wind_staerke = self.get_wind_staerke(datum_hour_string)
        wind_richtung = self.get_wind_richtung(datum_hour_string)

        sonnen_stunden = self.get_sonnen_stunden(datum_string)
        niederschlag_menge = self.get_niederschlag_menge(datum_string)

        if luft_temp:
            return_list = [
                (day_string + '_wasser_temperatur', str(wasser_temp)),
                (day_string + '_luft_temperatur', str(luft_temp)),
                (day_string + '_relative_luft_feuchte', str(relative_feuchte)),
                (day_string + '_boden_temperatur_5cm', str(boden_temp_5)),
                (day_string + '_boden_temperatur_10cm', str(boden_temp_10)),
                (day_string + '_boden_temperatur_20cm', str(boden_temp_20)),
                (day_string + '_boden_temperatur_50cm', str(boden_temp_50)),
                (day_string + '_boden_temperatur_100cm', str(boden_temp_100)),
                (day_string + '_wind_staerke', str(wind_staerke)),
                (day_string + '_wind_richtung', str(wind_richtung)),
                (day_string + '_sonnen_stunden', str(sonnen_stunden)),
                (day_string + '_niederschlag_menge', str(niederschlag_menge)),
            ]
        else:
            return_list = []

        return return_list

    def get_full_class_value(self, fish_class, hour_24_int, date_int):

        return_list = [
            ('datum_monat_tag', str(date_int)),
            ('fangzeit_24_stunden', str(hour_24_int)),
            ('class_label', str(fish_class)),
        ]

        return return_list

    def get_second_tuple_value(self, data_tuple_list):
        return [value for key, value in data_tuple_list]

    def get_first_tuple_values(self, data_tuple_list):
        return [key for key, value in data_tuple_list]

    def generate_output_list(self, label_list, data_list):

        return_list = list()

        return_list.append("")
        return_list.append("@RELATION AngelDaten")

        for label_item in label_list:

            if label_item == 'class_label':
                return_list.append("@ATTRIBUTE class {Karpfen, Forelle, Brachse, Barbe, Hecht, Aal}")
            else:
                return_list.append("@ATTRIBUTE %s NUMERIC" % label_item)

        return_list.append("")
        return_list.append("@DATA")

        for data_point in data_list:
            data_string = ','.join(data_point)
            return_list.append(data_string)

        self.output_line_list = return_list

    def merge_data_attributes(self):

        counter = 0

        for fish_class, datum_string, datum_hour_string, hour_24_int, date_int in self.fish_catch_values:

            full_data_set = []

            for previous_day in range(0, self.MAX_PREVIOUS_DAYS):
                current_date = self.get_previous_date(datum_string, previous_day)
                current_hour_date = self.get_previous_hour_date(datum_hour_string, previous_day)

                data_value_tuples = self.get_full_tuple_values(current_hour_date, current_date, str(previous_day))
                data_points = self.get_second_tuple_value(data_value_tuples)

                if counter == 0:
                    day_labels = self.get_first_tuple_values(data_value_tuples)
                    self.arff_label_values.extend(day_labels)

                full_data_set.extend(data_points)

            if full_data_set:
                data_value_tuples = self.get_full_class_value(fish_class, hour_24_int, date_int)
                data_points = self.get_second_tuple_value(data_value_tuples)

                if counter == 0:
                    class_labels = self.get_first_tuple_values(data_value_tuples)
                    self.arff_label_values.extend(class_labels)

                full_data_set.extend(data_points)

                self.arff_data_values.append(full_data_set)

            counter += 1

        self.generate_output_list(self.arff_label_values, self.arff_data_values)

    def print_output_data(self):
        for row in self.output_line_list:
            print(row)

    def store_output_data(self):
        with open('output_arff.csv', 'w') as file:
            for line in self.output_line_list:
                file.write(line)
                file.write("\n")


# Klimadaten stand 2018 März
# Fangbuch stand 2017
s = FangBuch()

s.read_wasser_temp('wetter_daten/wassertemperatur/wassertemperatur_603100044.csv')
s.read_luft_temp_luft_feuchte('wetter_daten/temperaturfeuchte/produkt_tu_stunde_19490101_20171231_00282.txt')
s.read_boden_temp('wetter_daten/bodentemperatur/produkt_eb_stunde_19490101_20171231_00282.txt')
s.read_wind('wetter_daten/windstaerke/produkt_ff_stunde_19490101_20171231_00282.txt')
s.read_sonnenstunden('wetter_daten/sonnenstunden/produkt_sd_stunde_19490101_20171231_00282.txt')
s.read_niederschlag('wetter_daten/niederschlag/produkt_rr_stunde_19490101_20171231_00282.txt')

s.read_input_data('rohdaten/fangbuch_gesamt.csv')

s.merge_data_attributes()

s.print_output_data()
s.store_output_data()
