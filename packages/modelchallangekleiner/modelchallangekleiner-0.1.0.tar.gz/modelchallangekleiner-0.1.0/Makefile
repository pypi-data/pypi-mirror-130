#################################################################################
# GLOBALS                                                                       #
#################################################################################

DATE = $(shell date +"%Y%m%d")
DEFAULT_DATASET_URL = https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls
SRC = modelchallangekleiner
TESTS = tests
MODELS = models
SRC_DATA = $(SRC)/data
SRC_MODEL = $(SRC)/model
CONTEXT_PATH = data

CONTEXT_DIR = data/context/
CONTEXT_MANAGEMENT_DIR = src/context
MANAGEMENT_DIR = src/managment


#################################################################################
# COMMANDS                                                                      #
#################################################################################


fetch_data:
	python $(SRC_DATA)/fetch_data.py \
						--date $(DATE) \
						--context_path  $(CONTEXT_PATH) \
						--dataset_url  $(DEFAULT_DATASET_URL)

train:
	python $(SRC_MODEL)/train.py \
						--date $(DATE) \
						--context_path  $(CONTEXT_PATH) \
						--output_model_path $(MODELS)

test:
	pytest $(TESTS)

## Run pipeline
all: fetch_data train