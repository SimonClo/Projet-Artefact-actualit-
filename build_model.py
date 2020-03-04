import argparse

from data_access import db_access
from preprocessing import preprocess
from modelling import modelling

import config

if __name__ == "__main__":
    db_access.main(config.PATH_RAW_ARCHIVES, config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
    preprocess.main(config.PATH_RAW_ARCHIVES, config.PATH_PROCESSED_ARCHIVES)
    modelling.main(config.PATH_PROCESSED_ARCHIVES, config.PATH_MODEL, config.PATH_SCORES)
    