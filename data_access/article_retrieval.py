import logging
import pickle as pkl
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.models import RawArticle
from data_access.db_access import Client

logger = logging.getLogger(__name__)

def main(outpath, host, port, user, password, db_name, archives=True, dev=False, dev_iterations=10):
    """Store all archives in a binary file
    
    Arguments:
        outpath {string} -- path to store all archives in
    """
    client = Client(host, port, db_name)
    client.connect(user, password)
    logger.info("fetching articles")
    issues = client.fetch_all_articles(archives=archives, dev=dev, dev_iterations=dev_iterations)
    with open(outpath,"wb") as f:
        pkl.dump(issues,f)
    client.close()

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("path",help="path to store binary archives in")
    parser.add_argument("host",help="database host")
    parser.add_argument("port",help="database port")
    parser.add_argument("user",help="username to use to connect")
    parser.add_argument("password",help="password of the user")
    parser.add_argument("db_name",help="database name")
    parser.add_argument("--archives",action="store_true",help="wether to fetch archives or recent articles")
    args = parser.parse_args()
    main(args.path, args.host, args.port, args.user, args.password, args.db_name, args.archives)