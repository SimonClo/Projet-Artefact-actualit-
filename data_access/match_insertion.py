import logging
import pickle as pkl
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.models import RawArticle
from data_access.db_access import Client

logger = logging.getLogger(__name__)

def main(inpath, host, port, user, password, db_name):
    """Insert all matches found in the database

    Arguments:
        inpath {string} -- path to get matches from
    """
    with open(inpath,"rb") as f:
        matches = pkl.load(f)

    client = Client(host, port, db_name)
    client.connect(user, password)
    for match in matches:
        client.insert_match(match)
    
    logger.info(f"inserted {len(matches)} matches")
    client.close()

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("path",help="path to get matches from")
    parser.add_argument("host",help="database host")
    parser.add_argument("port",help="database port")
    parser.add_argument("user",help="username to use to connect")
    parser.add_argument("password",help="password of the user")
    parser.add_argument("db_name",help="database name")
    args = parser.parse_args()
    main(args.path, args.host, args.port, args.user, args.password, args.db_name)