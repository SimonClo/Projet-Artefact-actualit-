import psycopg2 as pg 
from models import Article
import logging
import pickle as pkl
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

def main(argv):
    """Store all articles in a binary file
    
    Arguments:
        argv {list(string)} -- string args, must provide path attribute
    """
    client = Client(config.DB_HOST,config.DB_PORT,config.DB_NAME)
    client.connect(config.DB_USER,config.DB_PASSWORD)
    issues = client.fetch_all_articles()
    with open(argv.path,"wb") as f:
        pkl.dump(issues,f)

class Client :
    """Database client to easily insert and fetch articles
    """
    def __init__(self,host,port,database):
        """Creates a client pointing to the given database
        
        Arguments:
            host {string} -- database host address
            port {int} -- port of the database server
            database {string} -- name of the database
        """
        self.host = host
        self.port = port
        self.database = database

    def connect(self,user,password):
        """Connect the client using the given credentials
        
        Arguments:
            user {string} -- username for the connection
            password {string} -- password of the given user
        """
        try :
            self.connection = pg.connect(
                user = user,
                password = password,
                database = self.database,
                host = self.host,
                port = self.port
            )
            self.cursor = self.connection.cursor()
            
        except (Exception, pg.Error) as error :
            logging.error("Connection failed",error)

    def fetch_all_articles(self):
        """Fetch all articles in the database
        
        Returns:
            list(Articles) -- a list of article objects
        """
        try :
            self.cursor.execute(
                '''
                SELECT * FROM articles
                '''
            )
            records = self.cursor.fetchall()
            articles = [Article(*record[1:]) for record in records]
            return articles
        except AttributeError as error :
            logging.error("Connection does not exist",error)
        except (Exception, pg.Error) as error :
            logging.error("Unable to retrieve articles",error)

    def insert_article(self,article):
        """Insert the given article in the database
        
        Arguments:
            article {Article object} -- the article to be inserted
        """
        try :
            insert_query = '''
                INSERT INTO articles(title,newspaper,published_date,url,article_text)
                VALUES (%s,%s,%s,%s,%s)
            '''
            values = (article.title, article.newspaper, article.date, article.url, article.text)
            self.cursor.execute(insert_query,values)
            self.connection.commit()
        except AttributeError as error :
            logging.error("Connection does not exist",error)
        except (Exception, pg.Error) as error :
            logging.error("Unable to insert",error)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("path",help="path to store binary articles in")
    args = parser.parse_args()
    main(args)
