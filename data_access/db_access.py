import psycopg2 as pg 
import logging
import pickle as pkl
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.models import RawArticle
import config

def main(argv):
    """Store all archives in a binary file
    
    Arguments:
        argv {list(string)} -- string args, must provide path attribute
    """
    client = Client(config.DB_HOST,config.DB_PORT,config.DB_NAME)
    client.connect(config.DB_USER,config.DB_PASSWORD)
    issues = client.fetch_all_archives()
    with open(argv.path,"wb") as f:
        pkl.dump(issues,f)

class Client :
    """Database client to easily insert and fetch archives
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
            
        except (Exception, pg.Error):
            logging.error("Connection failed")

    def fetch_all_archives(self):
        """Fetch all archives in the database
        
        Returns:
            list(archives) -- a list of article objects
        """
        try :
            self.cursor.execute(
                '''
                SELECT * FROM archives
                '''
            )
            records = self.cursor.fetchall()
            archives = [RawArticle(*record[1:]) for record in records]
            if config.DEV_MODE : archives = archives[:config.DEV_MODE_ITERATIONS]
            return archives
        except AttributeError:
            logging.error("Connection does not exist")
        except (Exception, pg.Error):
            logging.error("Unable to retrieve archives")

    def insert_archive(self,article):
        """Insert the given article in the database
        
        Arguments:
            article {Article object} -- the article to be inserted
        """
        try :
            insert_query = '''
                INSERT INTO archives(title,newspaper,published_date,url,article_text)
                VALUES (%s,%s,%s,%s,%s)
            '''
            values = (article.title, article.newspaper, article.date, article.url, article.text)
            self.cursor.execute(insert_query,values)
            self.connection.commit()
        except AttributeError:
            logging.error("Connection does not exist")
        except (Exception, pg.Error):
            logging.error("Unable to insert")

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("path",help="path to store binary archives in")
    args = parser.parse_args()
    main(args)
