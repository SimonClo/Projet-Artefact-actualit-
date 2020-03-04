import sys
import os
import argparse
import logging
import nltk
import pickle as pkl
from nltk import word_tokenize
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
from stop_words import get_stop_words

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.models import RawArticle, SplitArticle, ProcessedCorpus

def main(inpath, outpath):
    """Split raw articles and preprocess them
    
    Arguments:
        inpath {string} -- path of the raw articles
        outpath {string} -- path where the corpus of split articles will be saved
    """
    # openning raw articles
    with open(inpath,"rb") as f:
        articles = pkl.load(f)
    
    # Creating stop words list
    stop_words = set(stopwords.words('french'))

    stop_words_to_add = ['a', 'peut', 's', 'plus', 'si', 'tout', 'ce', 'cette', 'mais', 'être',
                        'c', 'comme', 'sans', 'aussi', 'fait', 'ça', 'an', 'sous', 'va', 'année', 'années', 'premier', 'premiers', 'première',
                        'vit', 'donner', 'donne', 'dernier', 'derniers', 'dernière', 'rien', 'reste', 'rester', 'bien', 'semain'
                        'autours', 'porte', 'prépare', 'préparer', 'trois', 'deux', 'quoi', 'quatre', 'cinq', 'six', 'sept', 'homme', 'jeune', 'france',
                        'entre', 'grand', 'grands', 'grande', 'grandes', 'après', 'partout', 'passe', 'jour', 'part', 'certains', 'certain',
                        'quelqu', 'aujourd', 'million', 'contre', 'pour', 'petit', 'ancien', 'demand', 'beaucoup', 'toujours'
                        'lorsqu', 'jusqu', 'hommme', 'seul', 'puis', 'faut', 'autr', 'toujour']
    stop_words_to_add += get_stop_words('fr')

    for word in stop_words_to_add:
        stop_words.add(word)

    # processing articles
    split_articles = []
    logging.info("tokenizing articles")
    for article in articles:
        split_text = tokenize(article.text)
        split_articles.append(SplitArticle(article.id,article.title,article.newspaper,article.date,article.url,split_text))
    corpus = ProcessedCorpus(split_articles)
    logging.info("removing stop words")
    corpus.apply_to_tokens_in_articles(lambda text: text.lower())
    corpus.apply_to_articles(lambda tokens: remove_stop_words(tokens,stop_words))
    logging.info("applying lemmatization")
    corpus.apply_to_tokens_in_articles(lemmatize)
    corpus.apply_to_articles(lambda tokens: remove_stop_words(tokens,stop_words))

    # saving processed corpus
    with open(outpath,"wb") as f:
        pkl.dump(corpus,f)  

def tokenize(text):
    """tokenize words in a text
    
    Arguments:
        text {string} -- a raw article to be tokenized
    
    Returns:
        {list(string)} -- tokenized text
    """
    without_punct = "".join([char if (char.isalnum() or char==" ") else " " for char in text])
    tokenized = word_tokenize(without_punct)
    return tokenized

def remove_stop_words(tokens,stop_words):
    """Remove all stop words from the article
    
    Arguments:
        tokens {list(string)} -- token list to remove stop words from
        stop_words {list(string)} -- list of stop_words to remove

    Returns:
        {list(string)} list of tokens without stop words
    """
    return [token for token in tokens if len(token)>3 and token not in stop_words]

def lemmatize(token):
    """Lemmatize word using a french lemmatizer
    
    Arguments:
        token {string} -- token to lemmatize
    """
    stemmer = FrenchStemmer()
    return stemmer.stem(token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inpath",help="path of the input file")
    parser.add_argument("outpath",help="path of the output file")
    args = parser.parse_args()
    main(args.inpath, args.outpath)

    
    
    

    
    
