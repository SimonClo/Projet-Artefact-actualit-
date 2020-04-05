from modelling.tf_idf import get_articles_keywords, get_keywords_from_text
from abc import ABC, abstractmethod
from tqdm import tqdm
import numpy as np
import copy
import logging
import re
from multiprocessing import cpu_count

import gensim
from gensim import corpora
from gensim.models.word2vec import Word2Vec
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.callbacks import CallbackAny2Vec

from modelling.force_topics import get_eta

logger = logging.getLogger(__name__)

class Model(ABC):
    """Base class for our NLP models
    """
    @abstractmethod
    def get_article_score(self, article):
        return {}

    def get_articles_scores(self):
        scores = []
        for article in tqdm(self.articles, desc="get articles scoring"):
            scores.append(self.get_article_score(article))
        return np.array(scores)

    def __init__(self, articles):
        """Create the model from the given arguments
        
        Arguments:
            articles {SplitArticles}
        """
        self.articles = articles #non splitted articles
        self.vocabulary = set()
        for article in articles : 
            self.vocabulary.update(article.tokens)

    def filter_vocab(self, article):
        """filter out the words that are not in the model's vocabulary
        
        Arguments:
            article {SplitArticle} -- new split article to filter
        """
        new_article = copy.deepcopy(article)
        new_article.tokens = [token for token in article.tokens if token in self.vocabulary]
        return new_article 

class TopicsModel(Model):

    def __init__(self, articles, words_no_above, num_topics, passes, iterations):
        """A LDA modeling based model
        
        Arguments:
            articles {list(SplitArticle)} -- List of articles in our corpus
            words_no_above {int} -- limit of occurence for words to be counted in the model
            num_topics {int} -- number of topics to find in the corpus
            passes {int} -- number of passes over the whole corpus
            iterations {int} -- max number of iterations through the corpus for inferring topic distribution
        """
        super().__init__(articles)
        self.words_no_above = words_no_above
        self.num_topics = num_topics
        self.passes = passes
        self.iterations = iterations
        self.train()
        self.scores = self.get_articles_scores()

    def train(self):
        split_archives = [article.tokens for article in self.articles]

        # create dictionary and corpus
        dictionary = corpora.Dictionary(split_archives)
        dictionary.filter_extremes(no_above=self.words_no_above)
        corpus = [dictionary.doc2bow(article) for article in split_archives]
        logger.info('Created dictionary and corpus')

        # get eta to force topics
        eta = get_eta(self.num_topics, dictionary)

        # create lda model with gensim
        lda_progress = LDAProgress(self.passes)
        ldamodel = LdaMulticore(
        corpus, num_topics = self.num_topics, id2word=dictionary, passes=self.passes, per_word_topics=True, 
            iterations=self.iterations, eta=eta, workers=cpu_count()
        )
        lda_progress.close()

        logger.info('Created Topics model')

        # print the topics (debug)
        logger.debug('Topics:')
        topics = ldamodel.print_topics(num_words=5)
        for topic in topics:
            logger.debug(topic)
        self.model = ldamodel
        self.dictionary = dictionary

    # get topic scores
    def get_article_score(self, article):
        article = self.filter_vocab(article)
        article_corpus = self.dictionary.doc2bow(article.tokens)
        topic_score = self.model.get_document_topics(article_corpus)

        return topic_score

class TfIdfModel(Model):

    def __init__(self, articles, num_keywords, words_no_above):
        """A Tf-Idf model
        
        Arguments:
            articles {list(SplitArticle)} -- split articles in our corpus
            num_keywords {int} -- number of keyword to represent the articles
            words_no_above {int} -- minimum number of occurence to be counted in the model
        """
        super().__init__(articles)
        self.num_keywords = num_keywords
        self.words_no_above = words_no_above
        texts = self.get_texts_from_splited_articles(articles)
        (self.scores, self.count_vectorizer, self.tf_idf_transformer) = get_articles_keywords(texts, self.num_keywords, self.words_no_above)

    # get tf idf keywords
    def get_article_score(self, article):
        article = self.filter_vocab(article)
        joined_article = " ".join(article.tokens)
        keywords_score = get_keywords_from_text(joined_article, self.num_keywords, self.tf_idf_transformer, self.count_vectorizer)

        return keywords_score

    def get_texts_from_splited_articles(self, splited_articles):
        """Auxiliary function : join the articles to be able to use scikit vectorizers
        """
        texts = []
        for article in splited_articles:
            text = ' '.join(article.tokens)
            texts.append(text)
        return texts

class Word2VecModel(Model):

    def __init__(self, articles, size, window, words_no_above, iterations):
        """A word2vec model wrapper 
        
        Arguments:
            articles {list(SplitArticles)} -- articles in the corpus
            size {int} -- size of the word vectors
            window {int} -- number of neigbouring words taken into account when training
            words_no_above {int} -- minimal number of occurence of a word to be kept
            iterations {int} -- number of epochs
        """
        super().__init__(articles)
        self.size = size
        self.window = window
        self.words_no_above = words_no_above
        self.iterations = iterations
        self.train()

    def train(self):
        token_lists = [article.tokens for article in self.articles]
        w2v_progress = W2VProgress(self.iterations)
        model = Word2Vec(sentences=token_lists, size = self.size, window = self.window, 
            min_count=self.words_no_above, workers=cpu_count(), iter=self.iterations, callbacks=[w2v_progress])
        w2v_progress.close()
        self.vocabulary = set(model.wv.vocab)
        model.init_sims(replace=True)
        self.model = model.wv

    def get_article_score(self, article):
        article = self.filter_vocab(article)
        article_vectors = []
        for token in article.tokens:
            article_vectors.append(self.model[token])
        return article_vectors



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

class W2VProgress(CallbackAny2Vec):

    def __init__(self, n_epochs):
        self.progress = tqdm(total = n_epochs, desc="processing word2vec : ")

    def on_batch_end(self, model):
        self.progress.update()

    def close(self):
        self.progress.close()
