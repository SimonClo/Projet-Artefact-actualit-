import sys
import os
import argparse
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_access.db_access import Client
from data_access.models import Article
import config


def parse_articles(filepath) :
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
                articles.append(Article(title,newspaper,date,url,text))
    return articles

def insert_all_articles(client,articles) :
    for article in articles :
        client.insert_article(article)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("filePath",help="path of parent directory of articles to insert")
    args = parser.parse_args()
    articles = parse_articles(args.filePath)
    client = Client(config.DB_HOST,config.DB_PORT,config.DB_NAME)
    client.connect(config.DB_USER,config.DB_PASSWORD)
    insert_all_articles(client,articles)


