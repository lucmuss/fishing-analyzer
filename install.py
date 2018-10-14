from tools.export_csv import export_to_mongodb

from tools.histograms import store_distributions
from tools.histograms import store_histograms
from tools.histograms import store_combined_histograms

from data.model import DatabaseModel
from data.model import FishFrameModel

database_model = DatabaseModel()

fish_model = FishFrameModel(database_model)

export_to_mongodb(database_model)

store_distributions(fish_model)
store_histograms(fish_model)
store_combined_histograms(fish_model)
