# coding: utf-8

from tools.import_db import import_to_db

from tools.histograms import store_distributions_separate
from tools.histograms import store_histograms_separate
from tools.histograms import store_histograms_summary

from data.model import ModelFactory

model_factory = ModelFactory()
database_model = model_factory.database_model
fish_frame_model = model_factory.fish_frame_model

import_to_db(database_model=database_model)

store_distributions_separate(fish_model=fish_frame_model)
store_histograms_separate(fish_model=fish_frame_model)
store_histograms_summary(fish_model=fish_frame_model)
