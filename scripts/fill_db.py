import sys
import os
import argparse
import json
from tqdm import tqdm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_access.db_access import Client
from utils.models import RawArticle
import config


def parse_articles(filepath) :
    """Parse all articles in the given directory and put them in a list
    
    Arguments:
        filepath {string} -- path of the directory containing all articles
    
    Returns:
        list(RawArticles) -- a list of parsed raw articles
    """
    articles = []
    for filename in os.listdir(filepath) :
        with open("/".join([filepath,filename]),"r") as file :
            read_file = json.loads(file.read())
            for article in read_file :
                title = article['title']
                text = article['text']
                date = filename.split(".")[0]
                newspaper = filepath.split("/")[-1]
                url = article['url']
                articles.append(RawArticle(len(articles),title,newspaper,date,url,text))
    return articles

def insert_all_articles(client,articles,archives) :
    """Insert all given articles in the database
    
    Arguments:
        client {Clietn} -- database client
        articles {list(RawArticles)} -- a list of raw articles
    """
    for article in tqdm(articles) :
        client.insert_article(article,archive=archives)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("filePath",help="path of parent directory of articles to insert")
    parser.add_argument("--archives",action="store_true",help="wether to store given articles in archives")
    parser.add_argument("--port", help="port of the db", type=int, default=config.DB_PORT)
    parser.add_argument("--user", help="username for the db", default=config.DB_USER)
    parser.add_argument("--host", help="host for the db", default=config.DB_HOST)
    parser.add_argument("--db-name", help="database name", default=config.DB_NAME)
    parser.add_argument("--password", help="password for the db user", default=config.DB_PASSWORD)
    args = parser.parse_args()
    client = Client(args.host, args.port, args.db_name)
    client.connect(args.user,args.password)
    articles = parse_articles(args.filePath)
    insert_all_articles(client,articles,args.archives)


