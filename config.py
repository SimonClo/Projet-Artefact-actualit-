import os
import sys
# database credentials

DB_HOST = "localhost"
DB_PORT = 8765
DB_NAME = "artefact_archives"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Dev mode for pipeline testing

DEV_MODE = False
DEV_MODE_ITERATIONS = 10

# Matching variables

NUM_MATCHES = 10

# Paths for the modelling pipeline

os.mkdir(os.path.join(os.getcwd(),"data"),exist_ok=True)
PATH_MODELLING = os.path.join(os.getcwd(),"data","modelling")
os.mkdir(PATH_MODELLING, exist_ok=True)
PATH_RAW_ARCHIVES = os.path.join(PATH_MODELLING,"raw_articles.pkl")
PATH_PROCESSED_ARCHIVES = os.path.join(PATH_MODELLING,"processed_articles.pkl")
PATH_MODEL = os.path.join(PATH_MODELLING,"model.pkl")
PATH_SCORES = os.path.join(PATH_MODELLING,"scores.pkl")