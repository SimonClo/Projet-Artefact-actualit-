# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: 'Python 3.6.9 64-bit (''artefact'': venv)'
#     language: python
#     name: python36964bitartefactvenvf543a7b80f284e37aec40cef7cfeffa6
# ---

# %% [markdown]
# # Word2vec for document similarities

# %% [markdown]
# We will try to explore the word2vec model to compute document similiarities. Each document, after preprocessing, is a list of more or less generalised tokens. By applying a TF-IDF algorithm, we are able to find which words best represent each document. However, when comparing two documents, comparing two document using their TF-IDF vectors can be quite slow due to the high dimension of the vectors representing each document, espacially with a corpus composed of newspaper archives. Comparing the top words for each document might be a better solution, if we are able to compute how far appart two different words can be. Word2vec allows us to bridge that gap by giving a vector representation to each word in the corpus.

# %% [markdown]
# ## Imports

# %%
import gensim
import nltk
import pickle as pkl
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

# %% [markdown]
# ## Test on a subset of the corpus

# %%
from gensim.models.word2vec import Word2Vec

with open("../data/dev_modelling/processed_articles.pkl","rb") as f:
    corpus = pkl.load(f)

print(len(corpus))
token_lists = [article.tokens for article in corpus]
model = Word2Vec(sentences=token_lists, size=100, window=5, min_count=2, workers=8)
model.init_sims(replace=True)

# %% [markdown]
# Once the model is trained, we can get vectors from any word in the corpus, and find the closest neighbours to any word.

# %%
print(list(model.wv.vocab)[100:130])
print(model.wv["europ"])
print(model.wv.most_similar("natal"))

# %% [markdown]
# Our interest is in finding the closest article to a new given article. for that we can use the word mover distance which computes the shortest flux to transform all words from an article to the other, given a word2vec model.

# %%
with open("../data/matching/articles_processed.pkl","rb") as f:
    new_articles = pkl.load(f)

print(f"new document : {new_articles[0].title}")
print(f"first archive : {corpus[0].title}")
print(f"second archive : {corpus[1].title}")

distance1 = model.wv.wmdistance(new_articles[0].tokens, corpus[0].tokens)
distance2 = model.wv.wmdistance(new_articles[0].tokens, corpus[1].tokens)
print(f"distance with first archive : {distance1}")
print(f"distance with second archive : {distance2}")


# %% [markdown]
# One thing worth to note is how much time takes the word mover distance, and how that duration can vary with the size of the different texts.

# %%
t0 = time.time()
distance1 = model.wv.wmdistance(new_articles[0].tokens, corpus[0].tokens)
t1 = time.time()

print(f"duration with full article ({len(new_articles[0].tokens)} tokens) : {t1 - t0} s")

t0 = time.time()
distance_short = model.wv.wmdistance(new_articles[0].tokens[:200], corpus[0].tokens)
t1 = time.time()

print(f"duration with shortened article (200 tokens) : {t1 - t0} s")

# %%
