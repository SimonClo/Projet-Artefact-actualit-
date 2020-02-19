import os
import sys
import argparse
import pickle as pkl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.models import RawArticle, SplitArticle, ProcessedCorpus

from gensim import corpora
import gensim
import logging
import numpy as np

import pyLDAvis
import pyLDAvis.gensim 

def get_titles_and_texts(corpus):
    titles = []
    articles = []
    for article in corpus.articles:
        titles.append(article.title)
        articles.append(article.tokens)
    logging.info('Created titles and articles')
    return (titles, articles)

def get_scores_from_documents_topics_matrix(documents_topics, nb_topics, corpus):
    scores = np.zeros((nb_topics, len(corpus)))
    for i in range(len(corpus)):
        for j in range(nb_topics):
            scores[j][i] = documents_topics[i][j][1]
    return(scores)

def main(argv):
    """
    Create a lda model and save it. Give to each article a score vector and save them.
    Args:
     - input path to corpus
     - output path for model
     - output path for score vector
    """
    # openning preprocessed articles
    with open(argv.inpath,"rb") as f:
        corpus = pkl.load(f)

    # Get titles and articles texts
    (titles, articles) = get_titles_and_texts(corpus)

    # Choose the parametres
    words_no_below = 0.8 # delete words that are in more than 0.8 of the articles
    NUM_TOPICS = 5

    # create dictionary and corpus
    dictionary = corpora.Dictionary(articles)
    dictionary.filter_extremes(no_below=words_no_below)
    corpus = [dictionary.doc2bow(article) for article in articles]
    logging.info('Created dictionary and corpus')

    # create lda model with gensim
    ldamodel = gensim.models.ldamodel.LdaModel(
    corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=10, per_word_topics=True, update_every=1, iterations=50
    )
    logging.info('Created gensim model')

    # print the topics (debug)
    logging.info('Topics:')
    topics = ldamodel.print_topics(num_words=5)
    for topic in topics:
        logging.info(topic)

    # Plot topics in a nice way (work in process ...)

    # save model in given outpath file
    ldamodel.save(argv.outpath_model)
    logging.info('Saved the model in '+argv.outpath_model)
    

    # get scores and save them
    get_document_topics = ldamodel.get_document_topics(corpus, minimum_probability=0.0)
    scores = get_scores_from_documents_topics_matrix(get_document_topics, NUM_TOPICS, corpus)
    with open(argv.outpath_scores,"wb") as f:
        pkl.dump(scores,f)


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("inpath",help="path to get preprocessed articles")
    parser.add_argument("outpath_model",help="path to store the model in")
    parser.add_argument("outpath_scores",help="path to store articles scores in")
    args = parser.parse_args()
    main(args)