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
# # Fonctions utiles avec nltk

# %% [markdown]
# Construisons quelques cas d'utilisation avec nltk

# %% [markdown]
# ## Imports

# %%
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import FrenchStemmer
import json



# %% [markdown]
# Il faut importer non seulement les modules, mais aussi, le corpus qui permet d'analyser le texte en langue française. La cellule suivante permet d'importer les fichier de corpus, et les stocke dans le dossier de l'utilisateur. 
#
# **Ne pas exécuter si vous avez déjà téléchargé les fichiers du corpus**

# %%
nltk.download("all-corpora")

# %% [markdown]
# On teste l'import du corpus français en affichant les stopwords :

# %%
# French stop words

print(set(stopwords.words('french')))

# %% [markdown]
# ### Différents types de tokenization

# %% [markdown]
# Par mot :

# %%
text = "Ceci est une phrase d'exemple pour démontrer l'action de différentes fonctions du module nltk. Ceci est "
text += "la deuxième phrase du texte d'exemple, car dans la tokenization il n'y a pas que la séparation par mot. "
text += "En effet il y aussi la séparation par phrase."

print(word_tokenize(text,language="french"))

# %% [markdown]
# Par phrase :

# %%
text = "Ceci est une phrase d'exemple pour démontrer l'action de différentes fonctions du module nltk. Ceci est "
text += "la deuxième phrase du texte d'exemple, car dans la tokenization il n'y a pas que la séparation par mot. "
text += "En effet il y aussi la séparation par phrase."

print(sent_tokenize(text,language="french"))

# %% [markdown]
# ### Filtrage des stopwords et de la ponctuation

# %%
# Filtering a sentence with stop words

text = "Ceci est une phrase d'exemple pour démontrer l'action de différentes fonctions du module nltk. Ceci est "
text += "la deuxième phrase du texte d'exemple, car dans la tokenization il n'y a pas que la séparation par mot. "
text += "En effet il y aussi la séparation par phrase."

#removing punctuation : 
text = "".join([char if (char.isalnum() or char==" ") else " " for char in text])

#removing stop words
stop_words = set(stopwords.words('french'))

words = word_tokenize(text)
print(" ".join(words)+"\n")
 
words_base = [word.lower() for word in words if word not in stop_words]

print(" ".join(words_base))

# %% [markdown]
# ### Comptage et affichage des occurences d'un mot

# %%
# Number of appearance of a word in a text

file = open('cleaned_articles/1956/09_11_1956.json', 'r')
read_file = json.loads(file.read())[0]['text']
text = nltk.Text(nltk.word_tokenize(read_file))

match = text.concordance('France')

# %% [markdown]
# ### Suppression des terminaisons

# %%
# Stemming

fs = FrenchStemmer()

words_stemmed = []
for word in words_base :
    words_stemmed.append(fs.stem(word))

print(" ".join(words_stemmed))

# %% [markdown]
# **Note:** On peut voir que le stemming enlève toutes les terminaisons sans distinctions dans cette utilisation, c'est une transformation trop radicale si on l'effectue sur chaque mot.

# %% [markdown]
# ### Lemmatisation

# %%
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()

other_stem = [stemmer.stem(word) for word in words_base]
print(" ".join(other_stem))
