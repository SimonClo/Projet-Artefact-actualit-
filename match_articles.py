from data_access import article_retrieval, match_insertion
from preprocessing import preprocess
from matching import match

import config

article_retrieval.main(config.PATH_RAW_ARTICLES, config.DB_HOST, config.DB_PORT, 
    config.DB_USER, config.DB_PASSWORD, config.DB_NAME, archives=False)
preprocess.main(config.PATH_RAW_ARTICLES, config.PATH_PROCESSED_ARTICLES)
match.main(config.PATH_PROCESSED_ARTICLES, config.PATH_MODELS, config.PATH_MATCHES, config.DISTANCE, config.NUM_MATCHES)
match_insertion.main(config.PATH_MATCHES, config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)