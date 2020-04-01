import sys
import os
import argparse
import pickle as pkl
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.models import RawArticle, SplitArticle

def main(inpath_articles, inpath_model, inpath_corpus_scores, outpath_matches, distance, num_matches=10):
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
        new_corpus = pkl.load(f)
    with open(inpath_model,"rb") as f:
        model = pkl.load(f)
    with open(inpath_corpus_scores,"rb") as f:
        score_matrix = pkl.load(f)
    
    distance = dispatch_distance(distance)
    article_matches = []
    for article in new_corpus.articles :
        new_score = model.score(article)
        best_matches = get_matching(score_matrix,new_score,distance,10)
        article_matches.append(best_matches)
    
    with open(outpath_matches,"wb") as f:
        pkl.dump(article_matches,f)

def dispatch_distance(name):
    """Return the distance function that matches name
    
    Arguments:
        name {string} -- name of the distance function
    
    Raises:
        Exception: Raise an exception if the given distance is not recognized
    
    Returns:
        function -- distance function
    """
    if name=="cosine":
        return cosine_similarity
    elif name=="euclidian":
        return euclidean_distances
    else:
        raise Exception(f"distance {name} not implemented")



def get_matching(score_matrix,new_score,distance,num_matches):
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
    distances = np.zeros((score_matrix.shape[0]))
    for i in range(score_matrix.shape[0]) :
        distances[i] = distance(score_matrix[i],new_score)
        sorted_indexes = np.argsort(distances)
    return sorted_indexes[:num_matches]

    

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("new_articles_path",help="path of the new article")
    parser.add_argument("model_path",help="path the trained model was stored in")
    parser.add_argument("scores_path",help="path the archives scores were stored in")
    parser.add_argument("distance",help="distance used to compute similarity")
    parser.add_argument("outpath",help="path to store the best matches in")
    args = parser.parse_args()
    main(args.new_articles_path, args.model_path, args.scores_path, args.outpath, args.distance)