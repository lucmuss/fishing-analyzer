from tools.export_csv import export_to_mongodb

from tools.histograms import store_distributions
from tools.histograms import store_histograms
from tools.histograms import store_combined_histograms

from data.model import fish_frame_model
from data.model import database_model

export_to_mongodb(database_model)

store_distributions(fish_frame_model)
store_histograms(fish_frame_model)
store_combined_histograms(fish_frame_model)
