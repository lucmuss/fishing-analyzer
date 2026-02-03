# coding: utf-8

import os
from typing import Any, List, Optional, Tuple

import numpy as np
import plotly
import plotly.figure_factory as ff
import plotly.graph_objs as go
import plotly.offline
import plotly.tools

import config
import utils
from utils import get_layout_dict, is_valid_fish_frame


def get_clean_values(attribute_series: Any) -> np.ndarray:
    """Konvertiert eine Serie von Attributwerten in einen bereinigten NumPy-Array,
    wobei NaN-Werte in Nullen umgewandelt werden.

    Args:
        attribute_series: Eine Pandas Series, die die Attributwerte enthält.

    Returns:
        Ein NumPy-Array mit bereinigten (numerischen) Werten.
    """
    attribute_values: np.ndarray = attribute_series.values
    cleaned_attribute_values: np.ndarray = np.nan_to_num(attribute_values, copy=True)
    return cleaned_attribute_values


def has_valid_data_values(cleaned_attribute_values: np.ndarray) -> bool:
    """Prüft, ob die bereinigten Attributwerte gültige Daten für die Diagrammerstellung enthalten.

    Dies ist der Fall, wenn der minimale Wert kleiner ist als der maximale Wert, was anzeigt,
    dass es eine Variation in den Daten gibt.

    Args:
        cleaned_attribute_values: Ein NumPy-Array mit bereinigten Attributwerten.

    Returns:
        True, wenn die Werte gültig sind, sonst False.
    """
    return cleaned_attribute_values.min() < cleaned_attribute_values.max()


def make_html_location(path_list: Optional[List[str]] = None, filename: str = '') -> str:
    """Erstellt den vollständigen Dateipfad für eine HTML-Ausgabedatei.

    Erstellt bei Bedarf die Verzeichnisstruktur.

    Args:
        path_list: Eine Liste von Verzeichnisnamen, die den Pfad zur Datei bilden.
        filename: Der Name der HTML-Datei (ohne Erweiterung).

    Returns:
        Der absolute Dateipfad zur HTML-Datei.
    """
    script_dir: str = os.getcwd()
    file_location_parts: List[str] = [script_dir]
    if path_list:
        file_location_parts.extend(path_list)

    file_location: str = os.path.join(*file_location_parts)

    if not os.path.exists(file_location):
        os.makedirs(file_location)

    file_path: str = os.path.join(file_location, f"{filename}.html")
    return file_path


def store_histograms_separate(fish_model: Any) -> None:
    """Speichert separate Histogramme für jeden Fischtyp und jedes Attribut als HTML-Dateien."""
    for fish_type in config.FISH_TYPES:
        fish_frame: Any = fish_model.get_fish_frame(fish_type)

        if is_valid_fish_frame(fish_frame):

            for attribute in fish_model.plotable_attributes:

                attribute_series: Any = fish_frame[attribute]
                cleaned_attribute_values: np.ndarray = get_clean_values(attribute_series)

                if has_valid_data_values(cleaned_attribute_values):
                    attribute_name: str = utils.attribute_to_name(attribute)
                    plot_title: str = utils.fish_and_attribute(fish_type, attribute_name)

                    data: List[go.Histogram] = [
                        go.Histogram(x=cleaned_attribute_values,
                                     name=attribute_name)]

                    layout_dict: Dict[str, Any] = get_layout_dict(title=plot_title)

                    layout: go.Layout = go.Layout(layout_dict)

                    figure: go.Figure = go.Figure(data=data, layout=layout)

                    file_path: str = make_html_location(path_list=["diagrams", "separate_histograms", fish_type],
                                                        filename=attribute)

                    plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_histograms_summary(fish_model: Any) -> None:
    """Speichert ein zusammenfassendes Histogramm für jeden Fischtyp als HTML-Datei."""
    for fish_type in config.FISH_TYPES:
        fish_frame: Any = fish_model.get_fish_frame(fish_type)

        if is_valid_fish_frame(fish_frame):

            subplots_titles: List[str] = [utils.attribute_to_name(attribute) for attribute in
                                          fish_model.plotable_attributes]

            number_attributes: int = len(fish_model.plotable_attributes)

            figure = plotly.tools.make_subplots(
                rows=number_attributes,
                cols=1, subplot_titles=subplots_titles)

            height_diagram: int = config.DIAGRAM_HEIGTH
            width_diagram: int = config.DIAGRAM_WIDTH

            final_height: int = height_diagram * number_attributes
            final_width: int = width_diagram * 1

            layout_dict: Dict[str, Any] = get_layout_dict(title=fish_type,
                                                          height=final_height,
                                                          width=final_width)

            figure['layout'].update(layout_dict)

            for index, attribute in enumerate(fish_model.plotable_attributes):

                attribute_series: Any = fish_frame[attribute]
                cleaned_attribute_values: np.ndarray = get_clean_values(attribute_series)

                if has_valid_data_values(cleaned_attribute_values):
                    attribute_to_name: str = utils.attribute_to_name(attribute)

                    counter: int = index + 1

                    trace: go.Histogram = go.Histogram(x=cleaned_attribute_values,
                                                             name=attribute_to_name)

                    figure.add_trace(trace, row=counter, col=1)

                    figure['layout']['xaxis{}'.format(counter)].update(
                        title='Werte'
                    )

                    figure['layout']['yaxis{}'.format(counter)].update(
                        title='Anzahl'
                    )

            file_path: str = make_html_location(path_list=["diagrams", "summary_histograms"], filename=fish_type)

            plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_distributions_summary(fish_model: Any) -> None:
    """Speichert zusammenfassende Verteilungs-Plots für jeden Fischtyp als HTML-Datei."""
    for fish_type in config.FISH_TYPES:
        fish_frame: Any = fish_model.get_fish_frame(fish_type)

        if is_valid_fish_frame(fish_frame):

            attribute_list: List[str] = list()
            attribute_value_list: List[List[Any]] = list()

            for index, attribute in enumerate(fish_model.plotable_attributes):
                attribute_series: Any = fish_frame[attribute]
                cleaned_attribute_values: np.ndarray = get_clean_values(attribute_series)

                if has_valid_data_values(cleaned_attribute_values):
                    attribute_name: str = utils.attribute_to_name(attribute)

                    attribute_list.append(attribute_name)
                    attribute_value_list.append(list(cleaned_attribute_values))

            figure = ff.create_distplot(hist_data=attribute_value_list,
                                            group_labels=attribute_list,
                                           )

            layout_dict: Dict[str, Any] = get_layout_dict(title=fish_type, y_title='Dichte')
            figure['layout'].update(layout_dict)

            file_path: str = make_html_location(path_list=["diagrams", "summary_distribution"],
                                                   filename=fish_type)

            plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_distributions_separate(fish_model: Any) -> None:
    """Speichert separate Verteilungs-Plots für jeden Fischtyp und jedes Attribut als HTML-Dateien."""
    for fish_type in config.FISH_TYPES:
        fish_frame: Any = fish_model.get_fish_frame(fish_type)

        if is_valid_fish_frame(fish_frame):

            for attribute in fish_model.plotable_attributes:

                attribute_series: Any = fish_frame[attribute]
                cleaned_attribute_values: np.ndarray = get_clean_values(attribute_series)

                if has_valid_data_values(cleaned_attribute_values):
                    attribute_name: str = utils.attribute_to_name(attribute)
                    plot_title: str = utils.fish_and_attribute(fish_type, attribute_name)

                    attribute_list: List[str] = [attribute_name]
                    attribute_value_list: List[List[Any]] = [list(cleaned_attribute_values)]

                    figure = ff.create_distplot(hist_data=attribute_value_list,
                                                            group_labels=attribute_list)

                    layout_dict: Dict[str, Any] = get_layout_dict(title=plot_title, y_title='Dichte')

                    figure['layout'].update(layout_dict)

                    file_path: str = make_html_location(path_list=["diagrams", "separate_distribution", fish_type],
                                                           filename=attribute)

                    plotly.offline.plot(figure, filename=file_path, auto_open=False)


if __name__ == '__main__':
    from data.model import ModelFactory

    model_factory: ModelFactory = ModelFactory()
    fish_frame_model: Any = model_factory.fish_frame_model

    store_distributions_summary(fish_model=fish_frame_model)
    store_distributions_separate(fish_model=fish_frame_model)
    store_histograms_separate(fish_model=fish_frame_model)
    store_histograms_summary(fish_model=fish_frame_model)
