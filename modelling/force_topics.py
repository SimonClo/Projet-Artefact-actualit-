# Create the topics
import numpy as np
import logging

logger = logging.getLogger(__name__)

# function to enter the topic in eta
def add_topic_to_eta(words, topic_nb, eta, dictionary):
    logger.info('Topic number '+str(topic_nb))
    for word in words:
        if word in dictionary.token2id:
            eta[topic_nb, dictionary.token2id[word]]*=10
        else:
            logger.info(f"{word} not in the dictionary")

# Functions that returns an eta matrix, depending on the n
def create_eta(topics, num_topics, dictionary):
    eta = np.ones((num_topics, len(dictionary)))*1/num_topics
    if num_topics < len(topics):
        logger.info('You try to seed to many topics')
        return None
    else:
        topic_nb = 0
        for topic in topics:
            add_topic_to_eta(topic, topic_nb, eta, dictionary)
            topic_nb += 1
    return eta

# special topics
words_sport = ['sport', 'olymp', 'athlet', 'défait', 'victoir', 'match', 'foot', 'champion', 'football', 'basket', 'roland', 'médaill', 'club', 'jeux', 'supporter'] # marche, associé à la tété chaine, cavle etc ...
words_ecology = ['durabl', 'planet', 'vert', 'ecolo', 'carbon', 'climat', 'écolog', 'énerg', 'nucléair', 'serr', 'gaz', 'réchauff']
words_school = ['scolair','écol','enseignement', 'enseign','étud','lycéen','orient','enfant', 'réform']
words_religion= ['églis', 'eglis', 'prêtr', 'vatican', 'relig', 'mess', 'évêqu', 'chrétien', 'catholic', 'catholique', 'cathol', 'abbé']
words_space = ['espac', 'astronaut', 'navet', 'spatial', 'lunair', 'satellit', 'apollo', 'terr', 'solair', 'orbit', 'cabin', 'oxygen']
words_shoah = ['juif', 'extermin', 'auschwitz', 'antisémit', 'camp', 'hitler', 'nazism', 'adolf', 'ghetto', 'rabbin', 'wagon', 'reich']
words_music = ['musiqu', 'concert', 'chanson', 'album']
words_seism = ['séism', 'humanitair', 'mort', 'trembl', 'terr']

topics = [words_ecology, words_sport, words_school, words_religion, words_space, words_shoah, words_music, words_seism]

def get_eta(num_topics, dictionary):
    return create_eta(topics, num_topics, dictionary)