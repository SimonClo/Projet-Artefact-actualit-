import psycopg2 as pg
import config
import logging

logger = logging.getLogger(__name__)

def connect():
    try :
        connection = pg.connect(
            user = config.DB_USER,
            password = config.DB_PASSWORD,
            database = config.DB_NAME,
            host = config.DB_HOST,
            port = config.DB_PORT
        )
        cursor = connection.cursor()
        return connection, cursor
        
    except (Exception, pg.Error):
        logger.error("Connection failed")


def get_latest_article(num_article):
    connection, cursor = connect()
    try :
        cursor.execute(
            '''
            SELECT title, published_date, url FROM recent_articles ORDER BY published_date DESC
            '''
        )
        records = cursor.fetchall()
        return records[num_article][0], records[num_article][2]

    except AttributeError:
        logger.error("Connection does not exist")
    except (Exception, pg.Error):
        logger.error("Unable to retrieve archives")
    finally:
        cursor.close()
        connection.close()