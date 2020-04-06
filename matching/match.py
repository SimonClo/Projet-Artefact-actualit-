import sys
import os
import argparse
import pickle as pkl
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from tqdm import tqdm
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

from utils.models import RawArticle, SplitArticle, Match
from matching.distances import cosine_distance, euclidian_distance, word_mover_distance

logger = logging.getLogger(__name__)

def main(inpath_articles, inpath_models, outpath_matches, distance, num_matches=10):
    """Score new processed articles using the trained model, and compare that score with the
    score of the archives articles, using the given distance
    
    Arguments:
        inpath_articles {string} -- path of the new split articles
        inpath_model {string} -- path of the trained model
        outpath_matches {string} -- path where the matches should be stored
        distance {string} -- name of the distance to be computed
        num_matches {int} -- number of matches to keep
    """
    with open(inpath_articles,"rb") as f:
        new_articles = pkl.load(f)
    with open(inpath_models,"rb") as f:
        (topics_model, tf_idf_model, word2vec_model) = pkl.load(f)
    logger.info(f"loaded {len(new_articles)} new articles")
    article_matches = []

    progress = tqdm(total=len(new_articles)*len(topics_model.articles), desc="processing matches : ")
    for article in new_articles :
        best_matches = get_matching(article, topics_model, tf_idf_model, word2vec_model, distance, config.NUM_MATCHES, progress)
        article_matches += best_matches
    progress.close()
    logger.info("matched articles")
    
    with open(outpath_matches,"wb") as f:
        pkl.dump(article_matches,f)

def get_similarity(index_archive, article, topics_model, tf_idf_model, word2vec_model, distance):
    """Return the distance function that matches name
    
    Arguments:
        index_archive {int} -- index of the archive we are matching
        article {SplitArticle} -- recent article we are matching
        topics_model {TopicsModel} -- trained lda model on the corpus
        tf_idf_model {TfIdfModel} -- trained tf-idf model on the corpus
        word2vec_model {Word2VecModel} -- trained word2vec_mode
        distance {string} -- distance we want to compute
    
    Raises:
        Exception: Raise an exception if the given distance is not recognized
    
    Returns:
        float -- similarity score between 0 and 1
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



def get_matching(article, topics_model, tf_idf_model, word2vec_model, distance, num_matches, progress=None):
    """Returns index of the best matches for the article
    
    Arguments:
        article {SplitArticle} -- recent article we are matching
        topics_model {TopicsModel} -- trained lda model on the corpus
        tf_idf_model {TfIdfModel} -- trained tf-idf model on the corpus
        word2vec_model {Word2VecModel} -- trained word2vec_mode
        distance {string} -- distance we want to compute
        num_matches {int} -- number of matches to be computed

    Keywords Arguments:
        progress {tqdm} -- progress bar for the matching (default: None)
    
    Returns:
        {list(Match)} -- list of index for articles in the score matrix
    """
    similarities = []
    for index_archive in range(len(topics_model.articles)) :
        similarities.append(get_similarity(index_archive, article, topics_model, tf_idf_model, word2vec_model, distance))
        if progress : progress.update()
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