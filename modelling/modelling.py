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
import config
from modelling.models import TfIdfModel, TopicsModel, Word2VecModel

logger = logging.getLogger(__name__)

def main(inpath, outpath):
    """
    Create a lda model and save it. Give to each article a score vector and save them.
    Args:
     - input path to corpus
     - output path for model and scores
    """
    # openning preprocessed articles
    with open(inpath,"rb") as f:
        archives = pkl.load(f)    

    # training all models
    topics_model = TopicsModel(archives, config.LDA_WORDS_NO_ABOVE, config.NUM_TOPICS, config.LDA_PASSES, config.LDA_ITERATIONS)
    tf_idf_model = TfIdfModel(archives, config.NUM_KEYWORDS, config.TF_IDF_WORDS_NO_ABOVE)
    word2vec_model = Word2VecModel(archives, config.W2V_SIZE, config.W2V_WINDOW, config.W2V_WORDS_NO_ABOVE, config.W2V_ITERATIONS)
    
    #saving models
    with open(outpath,"wb") as f:
        pkl.dump((topics_model, tf_idf_model, word2vec_model),f)
    logging.info('Saved the model in '+outpath)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("inpath",help="path to get preprocessed articles")
    parser.add_argument("outpath",help="path to store the model in")
    parser.add_argument("-v","--verbose", action="store_true", help="verbosity for gensim in particular")
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())

    main(args.inpath, args.outpath)