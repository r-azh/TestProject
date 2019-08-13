# This code is supporting material for the book
# Building Machine Learning Systems with Python
# by Willi Richert and Luis Pedro Coelho
# published by PACKT Publishing
#
# It is made available under the MIT License

import os

# DATA_DIR = "data"  # put your posts-2012.xml into this directory
DATA_DIR = os.path.sep.join(['C:', '_Data_', 'topc', 'ML_data', 'ch05'])

CHART_DIR = "charts"

filtered = os.path.join(DATA_DIR, "filtered.tsv")
filtered_meta = os.path.join(DATA_DIR, "filtered-meta.json")

chosen = os.path.join(DATA_DIR, "chosen.tsv")
chosen_meta = os.path.join(DATA_DIR, "chosen-meta.json")
