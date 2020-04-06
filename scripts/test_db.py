import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_access.db_access import Client
from utils.models import RawArticle
import config

if __name__ == "__main__" :
    client = Client(config.DB_HOST,config.DB_PORT,config.DB_NAME)
    client.connect(config.DB_USER,config.DB_PASSWORD)
    articles = client.fetch_all_articles()
    print(len(articles))