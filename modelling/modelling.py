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

from tf_idf import get_articles_keywords
from force_topics import get_eta

def get_titles_and_texts(corpus):
    titles = []
    articles = []
    for article in corpus.articles:
        titles.append(article.title)
        articles.append(article.tokens)
    logging.info('Created titles and articles')
    return (titles, articles)

def get_scores_from_documents_topics_matrix(documents_topics, nb_topics, corpus):
    scores = [[0]*nb_topics]*len(corpus)
    for i in range(len(corpus)):
        for j in range(nb_topics):
            scores[i][j] = documents_topics[i][j][1]
    return(scores)

def get_texts_from_splited_articles(splited_articles):
    texts = []
    for article in splited_articles:
        text = ' '.join(article)
        texts.append(text)
    return texts


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

    # Get non splited texts for tf_idf
    texts = get_texts_from_splited_articles(articles)

    # Choose the parametres
    words_no_above = 0.6 # delete words that are in more than ... of the articles, works for topic modelling and keywords !
    NUM_TOPICS = 5

    # create dictionary and corpus
    dictionary = corpora.Dictionary(articles)
    dictionary.filter_extremes(no_above=words_no_above)
    corpus = [dictionary.doc2bow(article) for article in articles]
    logging.info('Created dictionary and corpus')

    # get eta to force topics
    eta = get_eta(NUM_TOPICS, dictionary)

    # create lda model with gensim
    ldamodel = gensim.models.ldamodel.LdaModel(
    corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=10, per_word_topics=True, update_every=1, iterations=50, eta=eta
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

    # get topics and keywords
    get_document_topics = ldamodel.get_document_topics(corpus, minimum_probability=0.0)
    topic_scores = get_scores_from_documents_topics_matrix(get_document_topics, NUM_TOPICS, corpus)

    # get article keywords
    keywords_scores = get_articles_keywords(texts, 20, words_no_above)

    # get scores and save them
    scores = np.array([{'topics': topic_scores[0], 'keywords': keywords_scores[0]}])
    for i in range(1, len(articles)):
        scores = np.append(scores, [{'topics': topic_scores[i], 'keywords': keywords_scores[i]}], axis=0)
    print(scores[0])

    with open(argv.outpath_scores,"wb") as f:
        pkl.dump(scores,f)


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("inpath",help="path to get preprocessed articles")
    parser.add_argument("outpath_model",help="path to store the model in")
    parser.add_argument("outpath_scores",help="path to store articles scores in")
    args = parser.parse_args()
    main(args)