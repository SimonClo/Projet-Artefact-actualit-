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

# %%
# !pip3 install pandas

# %%
import pandas as pd

# %%
# On met tous les articles dans un Dataframe Panda, en y ajoutant l'année et le jour et la taille
path = "Downloads/cleaned_articles"

import os
import json
all_json_documents = []
all_articles = []

years = os.listdir(path)
del years[0]  #le premier dossier n'est pas une année

for year in years:
    for filename in os.listdir(path + "/" + year):
        f = open("Downloads/cleaned_articles/" + year + "/" + filename, 'r')
        json_document = f.read()
        json_document = json.loads(json_document)
        all_json_documents.append(json_document)
        for article in json_document:
            article['year'] = year
            article['date'] = filename[:len(filename) - 5] #retirer le .json
            article['size'] = len(article['text'])
            all_articles.append(article)

articles_df = pd.DataFrame(all_articles, columns=["year", "date", "title", "text", 'url', 'size'])
articles_df[:3]

# %%
import matplotlib.pyplot as plt

# Nombre d'articles en tout
nb_articles = len(articles_df.index)
print("Nombres d'articles : ", nb_articles, '\n')

# Nombre d'articles en fonction des années
years = articles_df['year']
years = list(map(int, years))
nb_years = articles_df['year'].value_counts().count()
plt.hist(years, bins=nb_years)
plt.gca().set(title="Nombre d'articles en fonction des années \n")
plt.show()


# %%
# Articles ou citations ? On affiche la taille des articles

plt.hist(articles_df['size'], bins=50)
plt.gca().set(title='Répartition des articles en fonction de leur taille')
plt.xlabel('Taille des articles en nb de caractères')
plt.ylabel('Nombre d\articles')
plt.show()



# %% [markdown]
# Il y a donc beaucoup d'articles avec peu de caractères, il y a dedans des citations ou des articles tronqués

# %%
# Afficher les titres des articles avec moins de 400 caractères

articles_df[articles_df['size'] < 400][['title', 'size', 'url']]


# %%

# quelques métriques
print("Quelques métriques: \n")
nb_less_400 = len(articles_df[articles_df['size'] < 400])
print("Poucentage d'articles à moins de 400 caractères : ", int(nb_less_400*100/nb_articles), "%")

nb_less_600 = len(articles_df[articles_df['size'] < 600])
print("Poucentage d'articles à moins de 600 caractères : ", int(nb_less_600*100/nb_articles), '%')

nb_less_800 = len(articles_df[articles_df['size'] < 800])
print("Poucentage d'articles à moins de 800 caractères : ", int(nb_less_800*100/nb_articles), '%')

# %%
