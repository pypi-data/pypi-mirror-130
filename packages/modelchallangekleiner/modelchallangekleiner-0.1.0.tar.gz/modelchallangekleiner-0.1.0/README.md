# challange-uci-cc-model

## Description

### Project structure

```
.
├── Dockerfile
├── Makefile
├── README.md
├── data                                    ### context path for all generated data
├── modelchallangekleiner                   ### src project folder
│   ├── __init__.py
│   ├── data                                ### scripts to download/generate data
│   │   ├── __init__.py
│   │   └── fetch_data.py
│   ├── features                            ### scripts to transform data for modelling
│   │   ├── __init__.py
│   │   ├── transformer.py
│   │   └── transformers
│   │       ├── __init__.py
│   │       └── custom_transformers.py
│   ├── model                               ### scripts to train and predict
│   │   ├── __init__.py
│   │   └── train.py
│   └── utils                               ### utils for all modules
│       ├── __init__.py
│       └── utils.py
├── models                                  ### output models path
├── poetry.lock
├── pyproject.toml
├── setup.py
└── tests                                   ### tests path
    ├── data
    │   └── test_fetch_data.py
    ├── features
    │   └── test_custom_transformers.py
    └── model
        ├── test_dataset
        │   └── uci_dataset.xls
        └── test_train.py
```

---

### Requirements

To run this repo you need:

- [docker](https://www.docker.com/)
- [poetry](https://python-poetry.org/)

### Setup

#### Run locally

follow the instructions below to run the repo locally.

```
poetry update
poetry shell
export PYTHONPATH=$PYTHONPATH:$(pwd)
make {fetch_data | train | test}
```

#### Run with docker

follow the instructions below to run the repo with docker.

```
docker build -t model_train:latest .
docker run -it model_train bash
make {fetch_data | train | test}
```

## Read

- [kaggle credit card problem](https://www.kaggle.com/lucabasa/credit-card-default-a-very-pedagogical-notebook#Introduction)
- [poetry](https://python-poetry.org/)
- [docker](https://www.docker.com/)


## Next steps

1. [ ] upload model.pkl to s3 bucket?
2. [ ] train different models?
3. [ ] add linters to github actions pipeline?
4. [ ] ...
