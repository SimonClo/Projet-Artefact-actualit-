import os
import sys
# database credentials

DB_HOST = "localhost"
DB_PORT = 8765
DB_NAME = "artefact_archives"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Dev mode for pipeline testing

DEV_MODE = True
DEV_MODE_ITERATIONS = 500

# Matching variables

NUM_MATCHES = 10

# Paths for the modelling pipeline

os.makedirs(os.path.join(os.getcwd(),"data"),exist_ok=True)
if DEV_MODE:
    PATH_MODELLING = os.path.join(os.getcwd(),"data","dev_modelling")
else:
    PATH_MODELLING = os.path.join(os.getcwd(),"data","modelling")
os.makedirs(PATH_MODELLING, exist_ok=True)
PATH_RAW_ARCHIVES = os.path.join(PATH_MODELLING,"raw_articles.pkl")
PATH_PROCESSED_ARCHIVES = os.path.join(PATH_MODELLING,"processed_articles.pkl")
PATH_MODEL = os.path.join(PATH_MODELLING,"model.pkl")
PATH_SCORES = os.path.join(PATH_MODELLING,"scores.pkl")