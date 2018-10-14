import plotly
import config
import os
import numpy

import plotly.figure_factory as figure_factory


def store_histograms(fish_model):
    for fish_type in config.ALLOWED_FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if fish_frame.size >= config.MINIMAL_CATCHED_FISHES:

            for attribute in fish_model.plotable_attributes:
                attribute_series = fish_frame[attribute]

                attribute_values = attribute_series.get_values()
                cleaned_attribute_values = numpy.nan_to_num(attribute_values, copy=True)

                if cleaned_attribute_values.min() != cleaned_attribute_values.max():
                    attribute_name = config.attribute_to_name(attribute)
                    plot_title = config.fish_and_attribute(fish_type, attribute_name)

                    data = [
                        plotly.graph_objs.Histogram(x=cleaned_attribute_values, nbinsx=config.HISTOGRAM_BINS,
                                                    name=attribute_name)]

                    layout = plotly.graph_objs.Layout(
                        title=plot_title,
                        xaxis=dict(
                            title='Werte'
                        ),
                        yaxis=dict(
                            title='Anzahl'
                        ),
                        bargap=0.1,
                        height=config.DIAGRAM_HEIGTH,
                        width=config.DIAGRAM_WIDTH
                    )

                    figure = plotly.graph_objs.Figure(data=data, layout=layout)

                    file_location = os.path.join("diagrams", "separate", fish_type)

                    if not os.path.exists(file_location):
                        os.makedirs(file_location)

                    file_path = os.path.join(file_location, "{}.html".format(attribute))

                    plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_combined_histograms(fish_model):
    for fish_type in config.ALLOWED_FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if fish_frame.size >= config.MINIMAL_CATCHED_FISHES:

            subplots_titles = [config.attribute_to_name(attribute) for attribute in
                               fish_model.plotable_attributes]

            number_attributes = len(fish_model.plotable_attributes)

            figure = plotly.tools.make_subplots(
                rows=number_attributes,
                cols=1, subplot_titles=subplots_titles)

            height_diagram = config.DIAGRAM_HEIGTH
            width_diagram = config.DIAGRAM_WIDTH

            final_height = height_diagram * number_attributes
            final_width = width_diagram * 1

            figure['layout'].update(height=final_height, width=final_width)
            figure['layout'].update(bargap=0.2)
            figure['layout'].update(title=fish_type)

            for index, attribute in enumerate(fish_model.plotable_attributes):
                attribute_series = fish_frame[attribute]

                attribute_values = attribute_series.get_values()
                cleaned_attribute_values = numpy.nan_to_num(attribute_values, copy=True)

                if cleaned_attribute_values.min() != cleaned_attribute_values.max():
                    attribute_to_name = config.attribute_to_name(attribute)

                    counter = index + 1

                    trace = plotly.graph_objs.Histogram(x=cleaned_attribute_values,
                                                        nbinsx=config.HISTOGRAM_BINS,
                                                        name=attribute_to_name)

                    figure.add_trace(trace, counter, 1)

                    figure['layout']['xaxis{}'.format(counter)].update(
                        title='Werte'
                    )

                    figure['layout']['yaxis{}'.format(counter)].update(
                        title='Anzahl'
                    )

            file_location = os.path.join("diagrams", "summary")

            if not os.path.exists(file_location):
                os.makedirs(file_location)

            file_path = os.path.join(file_location, "{}.html".format(fish_type))

            plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_distributions(fish_model):
    for fish_type in config.ALLOWED_FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if fish_frame.size >= config.MINIMAL_CATCHED_FISHES:

            for attribute in fish_model.plotable_attributes:
                attribute_series = fish_frame[attribute]

                attribute_values = attribute_series.get_values()

                cleaned_attribute_values = numpy.nan_to_num(attribute_values, copy=True)

                if cleaned_attribute_values.min() != cleaned_attribute_values.max():

                    attribute_name = config.attribute_to_name(attribute)
                    plot_title = config.fish_and_attribute(fish_type, attribute_name)

                    attribute_list = [attribute_name]
                    attribute_value_list = [list(cleaned_attribute_values)]

                    figure = figure_factory.create_distplot(hist_data=attribute_value_list,
                                                            group_labels=attribute_list)

                    figure['layout'].update(title=plot_title,
                                            xaxis=dict(
                                                title='Werte'
                                            ),
                                            yaxis=dict(
                                                title='Anzahl'
                                            ),
                                            bargap=0.1,
                                            height=config.DIAGRAM_HEIGTH,
                                            width=config.DIAGRAM_WIDTH
                                            )

                    file_location = os.path.join("diagrams", "distribution", fish_type)

                    if not os.path.exists(file_location):
                        os.makedirs(file_location)

                    file_path = os.path.join(file_location, "{}.html".format(attribute))

                    plotly.offline.plot(figure, filename=file_path, auto_open=False)
