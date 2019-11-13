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

# %%
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import FrenchStemmer
import json

nltk.download('stopwords')
nltk.download('punkt')

# %%
# French stop words

print(set(stopwords.words('French')))

# %%
# Filtering a sentence with stop words

text = "Ceci est une phrase test pour savoir lesquels de mes mots seront supprimés avec le dictionnaire de stop words, j'ai."
stop_words = set(stopwords.words('french'))
words = word_tokenize(text)
print(words)
 
new_sentence = [word for word in words if word not in stop_words]
 
print(new_sentence)

# %%
# Number of appearance of a word in a text

file = open('cleaned_articles/1956/09_11_1956.json', 'r')
read_file = json.loads(file.read())[0]['text']
text = nltk.Text(nltk.word_tokenize(read_file))
 
match = text.concordance('France')

# %%
# Tokenize a sentence

nltk.sent_tokenize(read_file)

# %%
# Stemming

fs = FrenchStemmer()

#words = ["conduite","conduire","conduit","conduisais","conduira"]
words = ["es","est","suis","sommes","êtes","sont"]

for word in words:
    print(fs.stem(word))
    
    
text = "Ceci est une phrase test pour savoir lesquels de mes mots seront supprimés avec le dictionnaire de stop words, j'ai."
stop_words = set(stopwords.words('french'))
words = word_tokenize(text)

for word in words:
    print(fs.stem(word))

# %%
