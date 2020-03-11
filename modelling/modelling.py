import os
import sys
import argparse
import pickle as pkl
from tqdm import tqdm

from gensim import corpora
import gensim
import logging
import numpy as np

import pyLDAvis
import pyLDAvis.gensim 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.models import RawArticle, SplitArticle
import re

from modelling.tf_idf import get_articles_keywords

logger = logging.getLogger(__name__)



def get_titles_and_texts(corpus):
    titles = []
    articles = []
    for article in corpus:
        titles.append(article.title)
        articles.append(article.tokens)
    logger.info('Created titles and articles')
    return (titles, articles)

def get_scores_from_documents_topics_matrix(documents_topics, nb_topics, corpus):
    scores = [[0]*nb_topics]*len(corpus)
    for i in tqdm(range(len(corpus)), desc="scoring topics on corpus"):
        for j in range(nb_topics):
            scores[i][j] = documents_topics[i][j][1]
    return(scores)

def get_texts_from_splited_articles(splited_articles):
    texts = []
    for article in splited_articles:
        text = ' '.join(article)
        texts.append(text)
    return texts


def main(inpath, outpath_model, outpath_scores):
    """
    Create a lda model and save it. Give to each article a score vector and save them.
    Args:
     - input path to corpus
     - output path for model
     - output path for score vector
    """
    # openning preprocessed articles
    with open(inpath,"rb") as f:
        corpus = pkl.load(f)

    # Get titles and articles texts
    (titles, articles) = get_titles_and_texts(corpus)

    # Get non splited texts for tf_idf
    texts = get_texts_from_splited_articles(articles)

    # Choose the parametres
    words_no_above = 0.6 # delete words that are in more than ... of the articles, works for topic modelling and keywords !
    NUM_TOPICS = 5

    # create dictionary and corpus
    dictionary = corpora.Dictionary(articles)
    dictionary.filter_extremes(no_above=words_no_above)
    corpus = [dictionary.doc2bow(article) for article in articles]
    logger.info('Created dictionary and corpus')

    # create lda model with gensim
    lda_progress = LDAProgress(10)
    ldamodel = gensim.models.ldamulticore.LdaMulticore(
        corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=10, per_word_topics=True, 
        iterations=50
    )
    lda_progress.close()

    logger.info('Created gensim model')

    # print the topics (debug)
    logger.debug('Topics:')
    topics = ldamodel.print_topics(num_words=5)
    for topic in topics:
        logger.debug(topic)

    # Plot topics in a nice way (work in process ...)

    # save model in given outpath file
    ldamodel.save(outpath_model)
    logger.info('Saved the model in '+outpath_model)

    # get topics and keywords
    get_document_topics = ldamodel.get_document_topics(corpus, minimum_probability=0.0)
    topic_scores = get_scores_from_documents_topics_matrix(get_document_topics, NUM_TOPICS, corpus)
    logger.info("evaluated scores on corpus")

    # get article keywords
    keywords_scores = get_articles_keywords(texts, 20, words_no_above)
    logger.info("computed most significant keyword for each article (TF-IDF)")

    # get scores and save them
    scores = np.array([{'topics': topic_scores[0], 'keywords': keywords_scores[0]}])
    for i in range(1, len(articles)):
        scores = np.append(scores, [{'topics': topic_scores[i], 'keywords': keywords_scores[i]}], axis=0)
    print(scores[0])

    with open(outpath_scores,"wb") as f:
        pkl.dump(scores,f)
    logger.info("saved scores in "+outpath_scores)

class LDAProgress:
    """A logger for progress of the LDA model
    """

    def __init__(self,n_iter):
        self.logger = logging.getLogger("gensim")
        self.logger.setLevel(logging.INFO)
        self.handler = FilterHandler(n_iter)
        self.logger.addHandler(self.handler)

    def close(self):
        self.handler.progress.close()
        self.logger.removeHandler(self.handler)

class FilterHandler(logging.StreamHandler):
    """A handler that intercepts logging event based on
    filtering rules
    """

    def __init__(self, n_epochs, stream=None):
        super().__init__(stream)
        self.epoch = 0
        self.progress = tqdm(total = n_epochs, desc="processing lda : ")
        self.n_epochs = n_epochs
        self.progress.update()

    def emit(self, record):
        try:
            msg = self.format(record)
            msg = record.getMessage()
            if re.match(r"^PROGRESS:*", msg):
                epoch = int(msg[15])
                if epoch != self.epoch:
                    self.epoch += 1
                    self.progress.update()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("inpath",help="path to get preprocessed articles")
    parser.add_argument("outpath_model",help="path to store the model in")
    parser.add_argument("outpath_scores",help="path to store articles scores in")
    parser.add_argument("-v","--verbose", action="store_true", help="verbosity for gensim in particular")
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())

    main(args.inpath, args.outpath_model, args.outpath_scores)