import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def sort_coo(coo_matrix):
    # sord by descending number of score
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

def get_keywords_from_text(doc, nb_vectors, tfidf_transformer, cv):
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
    
    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    
    #extract only the top n
    feature_names=cv.get_feature_names()
    keywords=extract_topn_from_vector(feature_names,sorted_items, nb_vectors)
    
    return keywords

def get_articles_keywords(articles, nb_vectors, words_no_above, progress=None):
    cv=CountVectorizer(max_df=words_no_above, min_df=0, max_features=10000)
    word_count_vector=cv.fit_transform(articles)

    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    scores = []
    for article in articles:
        scores.append(get_keywords_from_text(article, nb_vectors, tfidf_transformer, cv))
        if progress : progress.update()
    
    return scores, cv, tfidf_transformer