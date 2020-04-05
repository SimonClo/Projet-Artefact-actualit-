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
DEV_MODE_ITERATIONS = 100

# Matching variables

NUM_MATCHES = 10
DISTANCE = "cosine"

# Paths for the modelling pipeline

os.makedirs(os.path.join(os.getcwd(),"data"),exist_ok=True)
if DEV_MODE:
    PATH_MODELLING = os.path.join(os.getcwd(),"data","dev_modelling")
else:
    PATH_MODELLING = os.path.join(os.getcwd(),"data","modelling")
os.makedirs(PATH_MODELLING, exist_ok=True)
PATH_RAW_ARCHIVES = os.path.join(PATH_MODELLING,"raw_articles.pkl")
PATH_PROCESSED_ARCHIVES = os.path.join(PATH_MODELLING,"processed_articles.pkl")
PATH_MODELS = os.path.join(PATH_MODELLING,"model.pkl")

# Paths for the matching pipeline

if DEV_MODE:
    PATH_MATCHING = os.path.join(os.getcwd(),"data","dev_matching")
else:
    PATH_MATCHING = os.path.join(os.getcwd(),"data","matching")
os.makedirs(PATH_MATCHING, exist_ok=True)
PATH_RAW_ARTICLES = os.path.join(PATH_MATCHING,"raw_articles.pkl")
PATH_PROCESSED_ARTICLES = os.path.join(PATH_MATCHING,"processed_articles.pkl")
PATH_MATCHES = os.path.join(PATH_MATCHING,"matches.pkl")

# Topic modeling

NUM_TOPICS = 5
LDA_WORDS_NO_ABOVE = 1
LDA_ITERATIONS = 50
LDA_PASSES = 10

# TF-IDF

TF_IDF_WORDS_NO_ABOVE = 2
NUM_KEYWORDS = 20

# Word2Vec

W2V_SIZE = 100
W2V_WINDOW = 5
W2V_WORDS_NO_ABOVE = 3
W2V_ITERATIONS = 10