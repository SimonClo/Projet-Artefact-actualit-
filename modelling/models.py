from modelling.tf_idf import get_articles_keywords
from abc import ABC, abstractmethod
from tqdm import tqdm
import numpy as np

class Model(ABC):
    """A representation of lda model with tf idf and topic modelling
    """
    @abstractmethod
    def get_article_score(self, article):
        return {}

    def get_articles_scores(self):
        scores = []
        for article in tqdm(self.articles, desc="get articles scoring"):
            scores.append(self.get_article_score(article))
        return np.array(scores)

    def __init__(self, model, articles, dictionary, num_keywords, words_no_above):
        """Create the model from the given arguments
        
        Arguments:
            model {ldamodel} -- ldamodel
            scores {np array} -- scores of each article of the corpus
        """
        self.model = model
        self.articles = articles #non splitted articles
        self.dictionary = dictionary
        self.num_keywords = num_keywords
        self.words_no_above = words_no_above
        self.scores = self.get_articles_scores()

class TopicsModel(Model):

    # get topic scores
    def get_article_score(self, article):
        article_corpus = self.dictionary.doc2bow([article])
        topic_score = self.model.get_document_topics(article_corpus)

        return topic_score

class TfIdfModel(Model):

    # get tf idf keywords
    def get_article_score(self, article):
        keywords_score = get_articles_keywords([article], self.num_keywords, self.words_no_above)[0]

        return keywords_score

class TopicsAndTfIdfModel(Model):

    # get scores about topic modelling and tf-idf
    def get_article_score(self, article):
        article_corpus = self.dictionary.doc2bow([article])
        topic_score = self.model.get_document_topics(article_corpus)

        keywords_score = get_articles_keywords([article], self.num_keywords, self.words_no_above)[0]

        return {'topics': topic_score, 'keywords': keywords_score}