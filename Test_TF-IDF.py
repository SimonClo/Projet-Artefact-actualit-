# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # TF-IDF

# %% [raw]
# sources: https://kavita-ganesan.com/extracting-keywords-from-text-tfidf/#Creating-Vocabulary-and-Word-Counts-for-IDF

# %% [markdown]
# ## Pre-process the articles

# %%
# #!pip3 install -U scikit-learn scipy matplotlib

# %%
import os
from math import *

import json
from nltk import word_tokenize
from stop_words import get_stop_words
import nltk
from nltk.corpus import stopwords

import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()

# %% [markdown]
# ### Creating list of stop-words

# %%
stop_words = set(stopwords.words('french'))

# add stop words
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

# %%
articles = []
processed_articles = []
titles = []
print('...')
for year in os.listdir('./cleaned_articles/'):
    if year != '.DS_Store':
        for filename in os.listdir('./cleaned_articles/'+year):
            if (len(articles)<5000):
                    path = './cleaned_articles/'+year+'/'+filename
                    file = open(path, 'r')
                    read_file = json.loads(file.read())
                    for article in read_file:
                        title = article['title']
                        article = article['text']

                        #removing punctuation, stop words and lemmatize
                        text = "".join([char if (char.isalnum() or char==" ") else " " for char in article])
                        text = word_tokenize(text)
                        text = [word.lower() for word in text if word.lower() not in stop_words]
                        text = [stemmer.stem(word) for word in text]
                        text = [word for word in text if len(word)>3 and word not in stop_words]
                        text = " ".join(text)
                        if len(text) > 200:
                            processed_articles.append(text)
                            articles.append(article)
                            titles.append(title)
                        if len(processed_articles)%100 == 0:
                            print(len(processed_articles))
print('Done')
print(len(processed_articles))


# %% [markdown]
# ## Creating Vocabulary and words count

# %%
#create a vocabulary of words, 
#ignore words that appear in 80% of documents, 
cv=CountVectorizer(max_df=0.85, min_df=0, stop_words=stop_words, max_features=10000)
word_count_vector=cv.fit_transform(processed_articles)

# %%
# display 10 firt words of our vocabulary
list(cv.vocabulary_.keys())[:5]

# %%
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)


# %%
# essentially sorts the values in the vector while preserving the column index.
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def get_kekwords_from_text(doc, nb_vectors):
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
    
    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    
    #extract only the top n; n here is 10
    keywords=extract_topn_from_vector(feature_names,sorted_items, nb_vectors)
    
    return keywords


# %%
# you only needs to do this once, this is a mapping of index to 
feature_names=cv.get_feature_names()
 
# get the document that we want to extract keywords from
articleNb=143
doc=processed_articles[articleNb]
title=titles[articleNb]
 
keywords = get_kekwords_from_text(doc, 10)
 
# now print the results
print("\n=====Doc=====")
print(title)
print("\n===Keywords===")
for k in keywords:
    print(k,keywords[k])


# %% [markdown]
# ## Try some matching

# %% [markdown]
# ### Some functions to calculate scores

# %%
#First try: for each doc take the 10 first words, and scores, and if there are the sames as the choosen articles,
# multiply there scores and add to score
def get_scores_simple(articles, target_article_keywords, nb_vectors):
    scores = []
    for article in articles:
        score = 0
        article_kws = get_kekwords_from_text(article, nb_vectors)
        for kword in target_article_keywords:
            for kw in article_kws:
                if kword == kw:
                    score += 1 - target_article_keywords[kword]*article_kws[kw]
                else:
                    score += 1
        scores.append(score)
    return(scores)


# %%
#Second try, some euclidian distance
def get_scores_with_euclidian_distance(articles, target_article_keywords, nb_vectors):
    scores = []
    for article in articles:
        score = 0
        article_kws = get_kekwords_from_text(article, nb_vectors)
        for kword in target_article_keywords:
            for kw in article_kws:
                if kword == kw:
                    score += (target_article_keywords[kword]-article_kws[kw])**2
                else:
                    score += 1
        scores.append(score)
    return(scores)


# %% [markdown]
# ### Choose and preprocess an article

# %%
#Choose an article
articleNb=146
target_article=processed_articles[articleNb]
title=titles[articleNb]

nb_vectors = 10

target_article_keywords = get_kekwords_from_text(target_article, nb_vectors)
 
# now print the results
print("\n=====Doc=====")
print(title)
print("\n===Keywords===")
for k in target_article_keywords:
    print(k,target_article_keywords[k])


# %% [markdown]
# ### Calculate scores related to our choosen article

# %%
print('...')
scores = get_scores_with_euclidian_distance(processed_articles, target_article_keywords, nb_vectors)
print('Done')

# %% [markdown]
# ### Find matches

# %%
nb_of_match_to_dislay = 3
results = scores[:]

# %%
for i in range(nb_of_match_to_dislay):
    index = scores.index(min(results))
    matched_article = processed_articles[index]
    article_kws = get_kekwords_from_text(matched_article, nb_vectors)
    print('\n Titre: ',titles[index])
    print("\n===Keywords===")
    for k in article_kws:
        print(k,article_kws[k])
    results[index]=100

# %% [raw]
# Les résultats restent très approximatifs, le matching ne donne pas de bons résultats.
# Améliorations à penser:
# - changer manière de calculer les scores (dstance euclidienne ? sur quoi ?)
# - tester avec plus d'articles
# - mélanger avec topic modelling
