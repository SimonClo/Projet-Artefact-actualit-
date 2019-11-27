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

import gensim
from gensim.models import CoherenceModel

import pyLDAvis
import pyLDAvis.gensim  
import matplotlib.pyplot as plt
# %matplotlib inline

from nltk.stem.snowball import FrenchStemmer


# +
#pip install stop-words
# -

# ### Create list of stop words

# +
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('french'))

# add stop words
stop_words_to_add = ['a', 'peut', 's', 'plus', 'si', 'tout', 'ce', 'cette', 'mais', 'être',
                     'c', 'comme', 'sans', 'aussi', 'fait', 'ça', 'an', 'sous', 'va', 'année', 'années', 'premier', 'premiers', 'première',
                     'vit', 'donner', 'donne', 'dernier', 'derniers', 'dernière', 'rien', 'reste', 'rester', 'bien', 'semain'
                    'autours', 'porte', 'prépare', 'préparer', 'trois', 'deux', 'quoi', 'quatre', 'cinq', 'six', 'sept', 'homme', 'jeune', 'france',
                    'entre', 'grand', 'grands', 'grande', 'grandes', 'après', 'partout', 'passe', 'jour', 'part', 'certains', 'certain',
                     'quelqu', 'aujourd', 'million', 'contre', 'pour', 'petit', 'ancien', 'demand', 'beaucoup', 'toujours'
                    'lorsqu', 'jusqu', 'hommme', 'seul']
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

stemmer = FrenchStemmer()
text = [stemmer.stem(word) for word in text]
text = [word for word in text if len(word)>3]
print(text)

# ### Create corpus and dictionary

# +
from gensim import corpora
from gensim.utils import simple_preprocess


# Create a dictionary, wich contains only words (tokens)
dictionary = corpora.Dictionary([text])


# Create corpus with data
corpus = [dictionary.doc2bow((token) for token in text)]

# Save them
import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

# +
import gensim
NUM_TOPICS = 4
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')

topics = ldamodel.print_topics(num_words=5)
for topic in topics:
    print(topic)
# -
# ## Work on several articles


# +
from gensim import corpora
from gensim.utils import simple_preprocess
import pickle

articles = []
print('...')
for year in os.listdir('./cleaned_articles/'):
    for filename in os.listdir('./cleaned_articles/'+year):
        if (len(articles)<10000):
                path = './cleaned_articles/'+year+'/'+filename
                file = open(path, 'r')
                read_file = json.loads(file.read())[0]['text']

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

NUM_TOPICS = 10
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


# +
# Show Topics
for topic in ldamallet.show_topics(formatted=False):
    print(topic)
    print()

# Visualize the topics
#pyLDAvis.enable_notebook()
#vis = pyLDAvis.gensim.prepare(ldamallet, corpus2, dictionary2)
#vis
# -

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




