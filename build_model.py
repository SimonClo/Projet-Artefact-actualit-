import argparse
import logging

from data_access import db_access
from preprocessing import preprocess
from modelling import modelling

import config

# Loggers setup
loggers = [logging.getLogger(name) for name in ["data_access","preprocessing","modelling"]]
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

# Main computation
db_access.main(config.PATH_RAW_ARCHIVES, config.DB_HOST, config.DB_PORT, config.DB_USER, 
    config.DB_PASSWORD, config.DB_NAME, dev=config.DEV_MODE, dev_iterations=config.DEV_MODE_ITERATIONS
)
preprocess.main(config.PATH_RAW_ARCHIVES, config.PATH_PROCESSED_ARCHIVES)
modelling.main(config.PATH_PROCESSED_ARCHIVES, config.PATH_MODEL, config.PATH_SCORES)
    