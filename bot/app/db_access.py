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
            SELECT id, title, published_date, url FROM recent_articles ORDER BY published_date DESC
            '''
        )
        records = cursor.fetchall()
        return records[num_article][0], records[num_article][1], records[num_article][3]

    except AttributeError:
        logger.error("Connection does not exist")
    except (Exception, pg.Error):
        logger.error("Unable to retrieve archives")
    finally:
        cursor.close()
        connection.close()


def get_matching_archive(article_id, archive_rank):
    connection, cursor = connect()
    try :
        get_query = '''
            SELECT a.title, a.url, a.published_date, m.score FROM archives a
            JOIN matches m ON a.id = m.id_archive
            WHERE m.id_recent_article = %s
            ORDER BY m.score DESC
        '''
        cursor.execute(get_query,(article_id,))
        records = cursor.fetchall()
        return records[archive_rank][0], records[archive_rank][1], records[archive_rank][2].split("_")[2]

    except AttributeError:
        logger.error("Connection does not exist")
    except (Exception, pg.Error):
        logger.error("Unable to retrieve archives")
    finally:
        cursor.close()
        connection.close()