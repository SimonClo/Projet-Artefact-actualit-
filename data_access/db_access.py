import psycopg2 as pg 
from utils.models import RawArticle
import logging

logger = logging.getLogger(__name__)

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

    def fetch_all_articles(self, archives=True, dev=True, dev_iterations=10):
        """Fetch all articles in the database
        
        Returns:
            list(archives) -- a list of article objects
        """
        try :
            if archives:
                self.cursor.execute(
                    '''
                    SELECT id, title, newspaper, published_date, url, article_text FROM archives
                    '''
                )
            else:
                self.cursor.execute(
                    '''
                    SELECT id, title, newspaper, published_date, url, article_text FROM recent_articles
                    '''
                )
            records = self.cursor.fetchall()
            articles = [RawArticle(*record) for record in records]
            if dev : articles = articles[:dev_iterations]
            return articles
        except AttributeError:
            logger.error("Connection does not exist")
        except (Exception, pg.Error):
            logger.error("Unable to retrieve archives")

    def insert_article(self,article,archive = True):
        """Insert the given archive in the database
        
        Arguments:
            article {Article object} -- the article to be inserted
        """
        try :
            if archive:
                insert_query = '''
                    INSERT INTO archives(title,newspaper,published_date,url,article_text)
                    VALUES (%s,%s,%s,%s,%s)
                '''
            else:
                insert_query = '''
                    INSERT INTO recent_articles(title,newspaper,published_date,url,article_text)
                    VALUES (%s,%s,%s,%s,%s)
                '''
            values = (article.title, article.newspaper, article.date, article.url, article.text)
            self.cursor.execute(insert_query,values)
            self.connection.commit()
        except AttributeError:
            logger.error("Connection does not exist")
        except (Exception, pg.Error):
            logger.error("Unable to insert")

    def insert_match(self, match):
        """Insert given match in the database
        
        Arguments:
            match {Match} -- Match object between two articles
        """
        try :
            insert_query = '''
                INSERT INTO matches(id_archive,id_recent_article,score)
                VALUES (%s,%s,%s)
            '''
            values = (match.id_archive, match.id_recent_article, match.score)
            self.cursor.execute(insert_query,values)
            self.connection.commit()
        except AttributeError:
            logger.error("Connection does not exist")
        except (Exception, pg.Error):
            logger.error("Unable to insert")


    def close(self):
        self.cursor.close()
        self.connection.close()
