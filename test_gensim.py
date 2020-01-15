# -*- coding: utf-8 -*-
# # Tests of topic modelling with gensim

# ### Import data

# + {"active": ""}
# Ressources
#
# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/

# +
import os
import json
from nltk import word_tokenize
from stop_words import get_stop_words
import nltk
from nltk.corpus import stopwords

import gensim
from gensim.models import CoherenceModel
from gensim import corpora
from gensim.utils import simple_preprocess

import pickle

import pyLDAvis
import pyLDAvis.gensim  
import matplotlib.pyplot as plt
# %matplotlib inline

from nltk.stem.snowball import FrenchStemmer

import pandas as pd

stemmer = FrenchStemmer()


# +
#pip install stop-words
# -

# ### Create list of stop words

# +
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
# -

# ## Work on one article

# ### Remove stop words and ponctuation

# +
# Create a list of words of first article
file = open('cleaned_articles/1956/13_01_1956.json', 'r')
read_file = json.loads(file.read())[0]['text']


#removing punctuation : 
text = "".join([char if (char.isalnum() or char==" ") else " " for char in read_file])
text = word_tokenize(text)

# remove stop words
text = [word.lower() for word in text if word.lower() not in stop_words]

# -

# ### Lemmatization

text = [stemmer.stem(word) for word in text]
text = [word for word in text if len(word)>3]
print(text)

# ### Create corpus and dictionary

# +
# Create a dictionary, wich contains only words (tokens)
dictionary = corpora.Dictionary([text])


# Create corpus with data
corpus = [dictionary.doc2bow((token) for token in text)]

# Save them
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

# +
NUM_TOPICS = 4
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')

topics = ldamodel.print_topics(num_words=5)
for topic in topics:
    print(topic)
# -
# ## Work on several articles


# +
articles = []
titles = []
print('...')
for year in os.listdir('./cleaned_articles/'):
    if year != '.DS_Store':
        for filename in os.listdir('./cleaned_articles/'+year):
            if (len(articles)<10000):
                    path = './cleaned_articles/'+year+'/'+filename
                    file = open(path, 'r')
                    read_file = json.loads(file.read())[0]
                    titles.append(read_file['title'])
                    read_file = read_file['text']

                    #removing punctuation, stop words and lemmatize
                    text = "".join([char if (char.isalnum() or char==" ") else " " for char in read_file])
                    text = word_tokenize(text)
                    text = [word.lower() for word in text if word.lower() not in stop_words]
                    text = [stemmer.stem(word) for word in text]
                    text = [word for word in text if len(word)>3 and word not in stop_words]
                    articles.append(text)
    
dictionary2 = corpora.Dictionary(articles)
corpus2 = [dictionary2.doc2bow(article) for article in articles]
pickle.dump(corpus2, open('corpus2.pkl', 'wb'))
dictionary2.save('dictionary2.gensim')
print('Done')
# -


# ### Create différent topics with gensim

# +
print('...')

NUM_TOPICS = 5
ldamodel2 = gensim.models.ldamodel.LdaModel(
    corpus2, num_topics = NUM_TOPICS, id2word=dictionary2, passes=15, per_word_topics=True, update_every=1
)
ldamodel2.save('model2.gensim')

ldamodel2 = gensim.models.ldamodel.LdaModel.load('model2.gensim')

topics2 = ldamodel2.print_topics(num_words=10)


for topic in topics2:
    print(topic)
    print()
# -
# ### Plot topics

# Visualize the topics
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(ldamodel2, corpus2, dictionary2)
vis

# ### Coherence and perplexity of this model

# +
#pip install pyLDAvis

# +
# Compute Perplexity
print('\nPerplexity: ', ldamodel2.log_perplexity(corpus2))  # a measure of how good the model is. lower the better.

# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=ldamodel2, texts=articles, dictionary=dictionary2, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)
# -

# ## Create topics with mallet 

# Download File: http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip
mallet_path = './mallet-2.0.8/bin/mallet'
ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus2, num_topics=5, id2word=dictionary2)


# Show Topics
for topic in ldamallet.show_topics(formatted=False):
    print(topic)
    print()

#Coherence
coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=articles, dictionary=dictionary2, coherence='c_v')
coherence_ldamallet = coherence_model_ldamallet.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet)


# ## Find optimal mallet model

def compute_coherence_values(limit, start=2, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary2 : Gensim dictionary
    corpus2 : Gensim corpus
    articles : List of input articles
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    mallet_path = './mallet-2.0.8/bin/mallet'
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        print(num_topics)
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus2, num_topics=num_topics, id2word=dictionary2)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=articles, dictionary=dictionary2, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


# Can take a long time to run.
limit=20
start=2
step=2
model_list, coherence_values = compute_coherence_values(start=start, limit=limit, step=step)

# Show graph
x = range(start, limit, step)
plt.plot(x, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.show()

#

# ### Give a document and find his dominant topic

# +
# Get document you want to see (last document)
# Create a list of words of first article
#file3 = open('cleaned_articles/1999/22_07_1999.json', 'r')
file3 = open('cleaned_articles/1999/29_07_1999.json', 'r') # Juifs marocains
read_file3 = json.loads(file3.read())[0]
title3 = read_file3['title']
text3 = read_file3['text']


#removing punctuation : 
text3 = "".join([char if (char.isalnum() or char==" ") else " " for char in text3])
text3 = word_tokenize(text3)

# remove stop words
text3 = [word.lower() for word in text3 if word.lower() not in stop_words]

text3 = [stemmer.stem(word) for word in text3]
text3 = [word for word in text3 if len(word)>3]



# Create a dictionary, wich contains only words (tokens)
dictionary3 = corpora.Dictionary([text3])


# Create corpus with data
corpus3 = [dictionary3.doc2bow((token) for token in text3)]

# -

def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


df_topic_sents_keywords = format_topics_sentences(ldamodel=ldamallet, corpus=corpus3, texts=title3)

# +
# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']

# Show
df_dominant_topic.head(15)
# + {}


df_topic_sents_keywords_2 = format_topics_sentences(ldamodel=ldamallet, corpus=corpus2, texts=titles)

# +
# Group top 5 sentences under each topic
sent_topics_sorteddf_mallet = pd.DataFrame()

sent_topics_outdf_grpd = df_topic_sents_keywords_2.groupby('Dominant_Topic')

for i, grp in sent_topics_outdf_grpd:
    sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet, 
                                             grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)], 
                                            axis=0)

# Reset Index    
sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)

# Format
sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]

# Show
sent_topics_sorteddf_mallet.head()
# + {}
#Future work to do
# Grid search, search best parameters with sklearn (see mail of Louise)
# -


