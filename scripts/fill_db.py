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
    args = parser.parse_args()
    articles = parse_articles(args.filePath)
    client = Client(config.DB_HOST,config.DB_PORT,config.DB_NAME)
    client.connect(config.DB_USER,config.DB_PASSWORD)
    insert_all_articles(client,articles,args.archives)


