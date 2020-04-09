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
DEV_MODE_ITERATIONS = 100

# Matching variables

NUM_MATCHES = 20
DISTANCE = "wordmover"

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
PATH_ALL_ARTICLES = os.path.join(PATH_MATCHING,"all_articles.pkl")
PATH_RAW_ARTICLES = os.path.join(PATH_MATCHING,"raw_articles.pkl")
PATH_PROCESSED_ARTICLES = os.path.join(PATH_MATCHING,"processed_articles.pkl")
PATH_MATCHES = os.path.join(PATH_MATCHING,"matches.pkl")

# Topic modeling

NUM_TOPICS = 20

LDA_ITERATIONS = 50
LDA_PASSES = 10

if DEV_MODE:
    LDA_WORDS_NO_ABOVE = 0.99
else:
    LDA_WORDS_NO_ABOVE = 0.6

# TF-IDF

if DEV_MODE:
    TF_IDF_WORDS_NO_ABOVE = 100
else:
    TF_IDF_WORDS_NO_ABOVE = 0.8
NUM_KEYWORDS = 20

# Word2Vec

W2V_SIZE = 100
W2V_WINDOW = 5
W2V_WORDS_NO_ABOVE = 3
W2V_ITERATIONS = 10
W2V_BATCH_SIZE = 10000