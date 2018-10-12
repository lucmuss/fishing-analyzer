import plotly
import config
import os

from data.model import FishFrameModel

fish_model = FishFrameModel()


def store_histograms():
    for fish_type in config.ALLOWED_FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if fish_frame.size:

            for attribute in fish_model.plotable_attributes:
                attribute_series = fish_frame[attribute]

                attribute_values = attribute_series.get_values()

                attribute_to_name = config.attribute_to_name(attribute)

                data = [plotly.graph_objs.Histogram(x=attribute_values, nbinsx=config.HISTOGRAM_BINS,
                                                    name=attribute_to_name)]

                layout = plotly.graph_objs.Layout(
                    title=attribute_to_name,
                    xaxis=dict(
                        title='Wertebereich'
                    ),
                    yaxis=dict(
                        title='Anzahl'
                    ),
                    bargap=0.1,
                )

                figure = plotly.graph_objs.Figure(data=data, layout=layout)

                file_location = os.path.join("diagrams", "separate", fish_type)

                if not os.path.exists(file_location):
                    os.makedirs(file_location)

                file_path = os.path.join(file_location, "{}.html".format(attribute))

                plotly.offline.plot(figure, filename=file_path, auto_open=False)


def store_combined_histograms():
    for fish_type in config.ALLOWED_FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if fish_frame.size:

            number_attributes = len(fish_model.plotable_attributes)

            figure = plotly.tools.make_subplots(
                rows=number_attributes,
                cols=2)

            height_diagram = 400
            width_diagram = 800

            figure['layout'].update(height=height_diagram * number_attributes, width=width_diagram * 2)
            figure['layout'].update(bargap=0.1)

            for index, attribute in enumerate(fish_model.plotable_attributes):
                attribute_series = fish_frame[attribute]

                attribute_values = attribute_series.get_values()

                attribute_to_name = config.attribute_to_name(attribute)

                trace = plotly.graph_objs.Histogram(x=attribute_values, nbinsx=config.HISTOGRAM_BINS,
                                                    name=attribute_to_name)

                figure.add_trace(trace, index + 1, (index % 2) + 1)

            file_location = os.path.join("diagrams", "summary")

            if not os.path.exists(file_location):
                os.makedirs(file_location)

            file_path = os.path.join(file_location, "{}.html".format(fish_type))

            plotly.offline.plot(figure, filename=file_path, auto_open=False)


store_histograms()
store_combined_histograms()
