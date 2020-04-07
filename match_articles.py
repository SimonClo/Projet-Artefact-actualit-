from data_access import article_retrieval, match_insertion, article_filtering
from preprocessing import preprocess
from matching import match

import config
import logging
import argparse

# Loggers setup
loggers = [logging.getLogger(name) for name in ["data_access","preprocessing","matching"]]
sysout = logging.StreamHandler()
formatter = logging.Formatter("%(name)s>%(levelname)s: %(message)s")
sysout.setFormatter(formatter)
for logger in loggers:
    logger.addHandler(sysout)

# Verbosity setup
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="display basic pipeline steps")
parser.add_argument("--debug", action="store_true", help="display more details about the pipeline")
args = parser.parse_args()
if args.verbose:
    for logger in loggers: logger.setLevel(logging.INFO)
elif args.debug:
    for logger in loggers: logger.setLevel(logging.DEBUG)
else:
    for logger in loggers: logger.setLevel(logging.WARNING)

article_retrieval.main(config.PATH_ALL_ARTICLES, config.DB_HOST, config.DB_PORT, 
    config.DB_USER, config.DB_PASSWORD, config.DB_NAME, archives=False)

article_filtering.main(config.PATH_ALL_ARTICLES, config.PATH_RAW_ARTICLES, config.DB_HOST, 
    config.DB_PORT, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)

preprocess.main(config.PATH_RAW_ARTICLES, config.PATH_PROCESSED_ARTICLES)
match.main(config.PATH_PROCESSED_ARTICLES, config.PATH_MODELS, config.PATH_MATCHES, config.DISTANCE, config.NUM_MATCHES)
match_insertion.main(config.PATH_MATCHES, config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
