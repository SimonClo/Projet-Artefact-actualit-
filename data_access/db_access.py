import psycopg2 as pg 
import logging
import pickle as pkl
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.models import RawArticle

logger = logging.getLogger(__name__)

def main(outpath, host, port, user, password, db_name, dev=False, dev_iterations=10):
    """Store all archives in a binary file
    
    Arguments:
        outpath {string} -- path to store all archives in
    """
    client = Client(host, port, db_name)
    client.connect(user, password)
    logger.info("fetching archives")
    issues = client.fetch_all_archives(dev, dev_iterations)
    with open(outpath,"wb") as f:
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
            logger.error("Connection failed")

    def fetch_all_archives(self, dev, dev_iterations):
        """Fetch all archives in the database
        
        Returns:
            list(archives) -- a list of article objects
        """
        try :
            self.cursor.execute(
                '''
                SELECT id, title, newspaper, published_date, url, article_text FROM archives
                '''
            )
            records = self.cursor.fetchall()
            archives = [RawArticle(*record) for record in records]
            if dev : archives = archives[:dev_iterations]
            return archives
        except AttributeError:
            logger.error("Connection does not exist")
        except (Exception, pg.Error):
            logger.error("Unable to retrieve archives")

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
            logger.error("Connection does not exist")
        except (Exception, pg.Error):
            logger.error("Unable to insert")

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("path",help="path to store binary archives in")
    parser.add_argument("host",help="database host")
    parser.add_argument("port",help="database port")
    parser.add_argument("user",help="username to use to connect")
    parser.add_argument("password",help="password of the user")
    parser.add_argument("db_name",help="dataabase name")
    args = parser.parse_args()
    main(args.path, args.host, args.port, args.user, args.password, args.db_name)
