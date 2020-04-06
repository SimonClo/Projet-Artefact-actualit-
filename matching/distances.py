from sklearn.metrics.pairwise import cosine_distances, euclidean_distances
import numpy as np

def cosine_distance(topics_model, new_article, index_archive):
    """Computes cosine distance using the topics model between recent article and archive
    
    Arguments:
        topics_model {TopicsModel} -- trained lda model
        new_article {SplitArticle} -- new article to match
        index_archive {int} -- index of the archive to match in the topics model scores
    
    Returns:
        float -- cosine distance between the two articles
    """
    score_archive = [elt[1] for elt in topics_model.scores[index_archive]]
    score_recent_article = [elt[1] for elt in topics_model.get_article_score(new_article)]
    return float(euclidean_distances(np.array(score_recent_article).reshape(1, -1), np.array(score_archive).reshape(1, -1)))

def euclidian_distance(topics_model, new_article, index_archive):
    """Computes euclidian distance using the topics model between recent article and archive
    
    Arguments:
        topics_model {TopicsModel} -- trained lda model
        new_article {SplitArticle} -- new article to match
        index_archive {int} -- index of the archive to match in the topics model scores
    
    Returns:
        float -- euclidian distance between the two articles
    """
    score_archive = [elt[1] for elt in topics_model.scores[index_archive]]
    score_recent_article = [elt[1] for elt in topics_model.get_article_score(new_article)]
    return float(euclidean_distances(np.array(score_recent_article).reshape(1, -1), np.array(score_archive).reshape(1, -1)))

def word_mover_distance(word2vec_model, tf_idf_model, new_article, index_archive):
    """Computes word mover distance using the word2vec between keywords of recent article and archive
    
    Arguments:
        word2vec_model {Word2VecModel} -- trained word2vec model
        tf_idf_model {TfIdfModel} -- trained tf-idf model
        new_article {SplitArticle} -- new article to match
        index_archive {int} -- index of the archive to match in the topics model scores
    
    Returns:
        float -- word mover distance between the two articles
    """
    keywords_archive = list(tf_idf_model.scores[index_archive].keys())
    keywords_recent_article = list(tf_idf_model.get_article_score(new_article).keys())
    return word2vec_model.model.wmdistance(keywords_archive, keywords_recent_article)
