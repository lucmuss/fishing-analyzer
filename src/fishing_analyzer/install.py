from fishing_analyzer.data.model import ModelFactory
from fishing_analyzer.tools.histograms import (
    store_distributions_separate,
    store_histograms_separate,
    store_histograms_summary,
)
from fishing_analyzer.tools.import_db import import_to_db


def main() -> None:
    model_factory = ModelFactory()
    database_model = model_factory.database_model
    fish_frame_model = model_factory.fish_frame_model

    import_to_db(database_model=database_model)
    store_distributions_separate(fish_model=fish_frame_model)
    store_histograms_separate(fish_model=fish_frame_model)
    store_histograms_summary(fish_model=fish_frame_model)


if __name__ == "__main__":
    main()
