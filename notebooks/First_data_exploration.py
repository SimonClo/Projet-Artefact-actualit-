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
# # Data Artefact

# %% [markdown]
# ## Imports

# %%
import numpy as np 
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

# %% [markdown]
# ## Lecture des articles

# %%
# putting all articles in a Dataframe, adding year, day, and size
path = "./data/L'express"

import os
import json
all_json_documents = []
all_articles = []

years = os.listdir(path)

for year in years:
    for filename in os.listdir(path + "/" + year):
        f = open(path+"/" + year + "/" + filename, 'r')
        json_document = f.read()
        json_document = json.loads(json_document)
        all_json_documents.append(json_document)
        for article in json_document:
            article['year'] = year
            article['date'] = filename[:len(filename) - 5] #stripping the .json extension
            article['size'] = len(article['text'])
            all_articles.append(article)

articles_df = pd.DataFrame(all_articles, columns=["year", "date", "title", "text", 'url', 'size'])
articles_df['size'].describe()

# %%
# number of articles in the complete set
nb_articles = len(articles_df.index)
print("# articles : ", nb_articles, '\n')

# number of articles per year
years = articles_df['year']
years = list(map(int, years))
nb_years = articles_df['year'].value_counts().count()
plt.hist(years, bins=nb_years)
plt.gca().set(title="# article per year \n")
plt.show()


# %% [markdown]
# **Note**: On illustre ici le fait que les articles sont très peu répartis dans le temps, il serait peut être nécessaire d'équilibrer le dataset en cherchant des articles plus anciens.

# %%
# displaying article size

plt.hist(articles_df['size'], bins=50)
plt.gca().set(title='distribution of articles according to size')
plt.xlabel('# of caracters per article')
plt.ylabel('# of articles')
plt.show()



# %% [markdown]
# **Note:** Il y a donc beaucoup d'articles avec peu de caractères, en isolant les articles avec peu de caractères, on se rend compte qu'il s'agit majoritairement de citations et d'articles tronqués.

# %%
# Displaying articles with less than 400 caracters

articles_df[articles_df['size'] < 400][['title', 'size', 'url']]


# %%
print("Some metrics on short articles: \n")
nb_less_400 = len(articles_df[articles_df['size'] < 400])
print("proportion of articles with less than 400 caracters : ", int(nb_less_400*100/nb_articles), "%")

nb_less_600 = len(articles_df[articles_df['size'] < 600])
print("proportion of articles with less than 600 caracters : ", int(nb_less_600*100/nb_articles), '%')

nb_less_800 = len(articles_df[articles_df['size'] < 800])
print("proportion of articles with less than 800 caracters : ", int(nb_less_800*100/nb_articles), '%')
