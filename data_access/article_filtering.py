import logging
import pickle as pkl
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.models import RawArticle
from data_access.db_access import Client
logger = logging.getLogger(__name__)

def main(inpath, outpath, host, port, user, password, db_name):
    """filter out all articles that already have matches
    
    Arguments:
        inpath {string} -- path to load recent articles from
        outpath {string} -- path to store all archives in
    """
    client = Client(host, port, db_name)
    client.connect(user, password)
    with open(inpath,"rb") as f:
        recent_articles = pkl.load(f)
    to_match = []
    for article in recent_articles:
        matches = client.get_match_recent_article(article.id)
        if len(matches) == 0:
            to_match.append(article)
    logger.info(f"extracted {len(to_match)} new articles without matches")
    with open(outpath,"wb") as f:
        pkl.dump(to_match,f)
    client.close()

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("inpath", help="path to get recent articles from")
    parser.add_argument("outpath",help="path to store binary archives in")
    parser.add_argument("host",help="database host")
    parser.add_argument("port",help="database port")
    parser.add_argument("user",help="username to use to connect")
    parser.add_argument("password",help="password of the user")
    parser.add_argument("db_name",help="database name")
    args = parser.parse_args()
    main(args.path, args.host, args.port, args.user, args.password, args.db_name, args.archives)