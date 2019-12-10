# Projet-Artefact-actualité

This project is a student project backed by the french data consulting company Artefact, aiming at the creation of an
archivist bot. This bot will be able to suggest archive articles related to recent news to the end user, based on a
matching algorithm leveraging the latest technologies in Natural Language processing.

## Prerequisites: 
- We use the jupytext module to simplify version control of jupyter notebooks, which allows easy conversions between notebooks
and python files.
install : `pip install jupytext`

## Directory structure:

App : main directory for the chatbot app
data_collection : usefull scripts for fetching articles from gallica

All data should be stored on the computer using the following hierarchy : 

```
.
|-data
  |-articles
    |-yyyy (year)
      |-dd_mm_yyyy.json (issue of the day)

```
