import psycopg2 as pg 
from data_access.models import Article
import logging

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
