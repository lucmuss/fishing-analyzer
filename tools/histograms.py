# coding: utf-8

import plotly
import config
import os
import numpy

import plotly.figure_factory as figure_factory

import utils
from utils import get_layout_dict, is_valid_fish_frame


def get_clean_values(attribute_series):
    attribute_values = attribute_series.get_values()
    cleaned_attribute_values = numpy.nan_to_num(attribute_values, copy=True)
    return cleaned_attribute_values


def has_valid_data_values(cleaned_attribute_values):
    return cleaned_attribute_values.min() < cleaned_attribute_values.max()


def make_html_location(path_list=None, filename=''):
    script_dir = os.getcwd()
    file_location = os.path.join(script_dir, *path_list)

    if not os.path.exists(file_location):
        os.makedirs(file_location)

    file_path = os.path.join(file_location, "{}.html".format(filename))
    return file_path


def store_histograms_separate(fish_model):
    for fish_type in config.FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if is_valid_fish_frame(fish_frame):

            for attribute in fish_model.plotable_attributes:

                attribute_series = fish_frame[attribute]
                cleaned_attribute_values = get_clean_values(attribute_series)

                if has_valid_data_values(cleaned_attribute_values):
                    attribute_name = utils.attribute_to_name(attribute)
                    plot_title = utils.fish_and_attribute(fish_type, attribute_name)

                    data = [
                        plotly.graph_objs.Histogram(x=cleaned_attribute_values,
                                                    name=attribute_name)]

                    layout_dict = get_layout_dict(title=plot_title)

                    layout = plotly.graph_objs.Layout(layout_dict)

                    figure = plotly.graph_objs.Figure(data=data, layout=layout)

                    file_path = make_html_location(path_list=["diagrams", "separate_histograms", fish_type],
                                                   filename=attribute)

                    plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_histograms_summary(fish_model):
    for fish_type in config.FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if is_valid_fish_frame(fish_frame):

            subplots_titles = [utils.attribute_to_name(attribute) for attribute in
                               fish_model.plotable_attributes]

            number_attributes = len(fish_model.plotable_attributes)

            figure = plotly.tools.make_subplots(
                rows=number_attributes,
                cols=1, subplot_titles=subplots_titles)

            height_diagram = config.DIAGRAM_HEIGTH
            width_diagram = config.DIAGRAM_WIDTH

            final_height = height_diagram * number_attributes
            final_width = width_diagram * 1

            layout_dict = get_layout_dict(title=fish_type,
                                          height=final_height,
                                          width=final_width)

            figure['layout'].update(layout_dict)

            for index, attribute in enumerate(fish_model.plotable_attributes):

                attribute_series = fish_frame[attribute]
                cleaned_attribute_values = get_clean_values(attribute_series)

                if has_valid_data_values(cleaned_attribute_values):
                    attribute_to_name = utils.attribute_to_name(attribute)

                    counter = index + 1

                    trace = plotly.graph_objs.Histogram(x=cleaned_attribute_values,
                                                        name=attribute_to_name)

                    figure.add_trace(trace, counter, 1)

                    figure['layout']['xaxis{}'.format(counter)].update(
                        title='Werte'
                    )

                    figure['layout']['yaxis{}'.format(counter)].update(
                        title='Anzahl'
                    )

            file_path = make_html_location(path_list=["diagrams", "summary_histograms"], filename=fish_type)

            plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_distributions_summary(fish_model):
    for fish_type in config.FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if is_valid_fish_frame(fish_frame):

            attribute_list = list()
            attribute_value_list = list()

            for index, attribute in enumerate(fish_model.plotable_attributes):
                attribute_series = fish_frame[attribute]
                cleaned_attribute_values = get_clean_values(attribute_series)

                if has_valid_data_values(cleaned_attribute_values):
                    attribute_name = utils.attribute_to_name(attribute)

                    attribute_list.append(attribute_name)
                    attribute_value_list.append(list(cleaned_attribute_values))

            figure = figure_factory.create_distplot(hist_data=attribute_value_list,
                                                    group_labels=attribute_list,
                                                    )

            layout_dict = get_layout_dict(title=fish_type, y_title='Dichte')
            figure['layout'].update(layout_dict)

            file_path = make_html_location(path_list=["diagrams", "summary_distribution"],
                                           filename=fish_type)

            plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_distributions_separate(fish_model):
    for fish_type in config.FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if is_valid_fish_frame(fish_frame):

            for attribute in fish_model.plotable_attributes:

                attribute_series = fish_frame[attribute]
                cleaned_attribute_values = get_clean_values(attribute_series)

                if has_valid_data_values(cleaned_attribute_values):
                    attribute_name = utils.attribute_to_name(attribute)
                    plot_title = utils.fish_and_attribute(fish_type, attribute_name)

                    attribute_list = [attribute_name]
                    attribute_value_list = [list(cleaned_attribute_values)]

                    figure = figure_factory.create_distplot(hist_data=attribute_value_list,
                                                            group_labels=attribute_list)

                    layout_dict = get_layout_dict(title=plot_title, y_title='Dichte')

                    figure['layout'].update(layout_dict)

                    file_path = make_html_location(path_list=["diagrams", "separate_distribution", fish_type],
                                                   filename=attribute)

                    plotly.offline.plot(figure, filename=file_path, auto_open=False)


if __name__ == '__main__':
    from data.model import ModelFactory

    model_factory = ModelFactory()
    fish_frame_model = model_factory.fish_frame_model

    store_distributions_summary(fish_model=fish_frame_model)
    store_distributions_separate(fish_model=fish_frame_model)
    store_histograms_separate(fish_model=fish_frame_model)
    store_histograms_summary(fish_model=fish_frame_model)
