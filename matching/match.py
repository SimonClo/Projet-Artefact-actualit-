import sys
import os
import argparse
import pickle as pkl
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

from utils.models import RawArticle, SplitArticle, Match
from matching.distances import cosine_distance, euclidian_distance, word_mover_distance

def main(inpath_articles, inpath_models, outpath_matches, distance, num_matches=10):
    """Score new processed articles using the trained model, and compare that score with the
    score of the archives articles, using the given distance
    
    Arguments:
        inpath_articles {string} -- path of the new split articles
        inpath_model {string} -- path of the trained model
        inpath_corpus_scores {string} -- path of the archive scores
        outpath_matches {string} -- path where the matches should be stored
        distance {string} -- name of the distance to be computed
    """
    with open(inpath_articles,"rb") as f:
        new_articles = pkl.load(f)
    with open(inpath_models,"rb") as f:
        (topics_model, tf_idf_model, word2vec_model) = pkl.load(f)
    
    article_matches = []
    for article in new_articles :
        best_matches = get_matching(article, topics_model, tf_idf_model, word2vec_model, distance, config.NUM_MATCHES)
        article_matches += best_matches
    
    with open(outpath_matches,"wb") as f:
        pkl.dump(article_matches,f)

def get_similarity(index_archive, article, topics_model, tf_idf_model, word2vec_model, distance):
    """Return the distance function that matches name
    
    Arguments:
        name {string} -- name of the distance function
    
    Raises:
        Exception: Raise an exception if the given distance is not recognized
    
    Returns:
        function -- distance function
    """

    if distance=="cosine":
        score_archive = [elt[1] for elt in topics_model.scores[index_archive]]
        score_recent_article = [elt[1] for elt in topics_model.get_article_score(article)]
        similarity = 1 - cosine_distance(score_recent_article, score_archive)
    elif distance=="euclidian":
        score_archive = [elt[1] for elt in topics_model.scores[index_archive]]
        score_recent_article = [elt[1] for elt in topics_model.get_article_score(article)]
        similarity = 1 - cosine_distance(score_recent_article, score_archive)
    else:
        raise Exception(f"distance {distance} not implemented")
    return similarity



def get_matching(article, topics_model, tf_idf_model, word2vec_model, distance, num_matches):
    """Returns index of the best matches for the article
    
    Arguments:
        score_matrix {np.ndarray(n_articles,dim_score)} -- matrix of scores from all articles
        new_score {np.ndarray(article)} -- score of the new article to compare with others
        distance {function(np.ndarra(score_dim),np.ndarray(score_dim))} -- distance used to compare the two articles
    
    Keyword Arguments:
        num_matches {int} -- number of matches to return (default: {10})
    
    Returns:
        {list(int)} -- list of index for articles in the score matrix
    """
    similarities = []
    for index_archive in range(len(topics_model.articles)) :
        similarities.append(get_similarity(index_archive, article, topics_model, tf_idf_model, word2vec_model, distance))
    sorted_indexes = np.argsort(similarities)[-num_matches:]
    return [Match(topics_model.articles[index].id, article.id, similarities[index]) for index in sorted_indexes]

    

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("new_articles_path",help="path of the new articles")
    parser.add_argument("models_path",help="path the trained model was stored in")
    parser.add_argument("distance",help="distance used to compute similarity")
    parser.add_argument("outpath",help="path to store the best matches in")
    args = parser.parse_args()
    main(args.new_articles_path, args.models_path, args.outpath, args.distance)