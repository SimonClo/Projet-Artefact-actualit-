from sklearn.metrics.pairwise import cosine_distances, euclidean_distances
import numpy as np

def cosine_distance(new_article_score, old_article_score):
    return float(cosine_distances(np.array(new_article_score).reshape(1, -1), np.array(old_article_score).reshape(1, -1)))

def euclidian_distance(new_article_score, old_article_score):
    return float(euclidean_distances(np.array(new_article_score).reshape(1, -1), np.array(old_article_score).reshape(1, -1)))

def word_mover_distance(word2vec_model, tf_idf_model, new_article, old_article):
    pass