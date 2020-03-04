import json
import os

def is_title(line) :
    """test if the current line is a title using an upper case heuristic
    
    Arguments:
        line {string} -- line of the text tested
    
    Returns:
        bool -- true if the given line is a title
    """
    upperCount = 0
    for char in line :
        if char.isupper() :
            upperCount += 1
    return upperCount/len(line) > 0.4 and len(line) < 70

def is_word(token) :
    """test if the given token is a word using an alphabetic lower case heuristic
    
    Arguments:
        token {string} -- the token to be tested
    
    Returns:
        bool -- true if the given token is a word
    """
    lowerCount = 0
    for char in token :
        if char.islower():
            lowerCount += 1
    if len(token) == 0 : return False
    else : return lowerCount/len(token) > 0.7

def get_articles(text) :
    """split the raw text from an article in title-article pairs by differentiating titles from the body of the text
    
    Arguments:
        text {string} -- the raw_text to split
    
    Returns:
        list of articles -- a list of dictionaries, each containing the title and body of the article
    """
    title = ""
    articles = []
    article = []
    wordCount = 0
    for line in text :
        if is_title(line) :
            if wordCount > 40 :
                articles.append({"title":title,"text":"\n".join(article)})
            wordCount = 0
            article = []
            title = line
        else : 
            count = len([token for token in line.split(" ") if is_word(token)])
            if count > 0 :
                wordCount += count
                article.append(line)
    return articles

def store_articles(issue,dirname) :
    """Storing articles in a json document in the given directory, with the publication date as name
    
    Arguments:
        issue {dict} -- an issue dictionnary
        issue-keys :
            date {string} -- date of the issue
            raw_text {list of string} -- the raw text of the issue
            url {string} -- url of the issue on gallica
        dirname {string} -- name of the directory to store articles in
    """ 
    structured_issue = []
    articles = get_articles(issue["raw_text"])
    for article in articles : 
        structured_issue.append({"title":article["title"],"text":article["text"],"url":issue["url"]})
    json_issue = json.dumps(structured_issue)
    if not os.path.isdir(dirname) :
        os.mkdir(dirname)
    correct_date = issue["date"].split("-")
    correct_date.reverse()
    with open(dirname+"/"+"_".join(correct_date)+".json","w") as f :
        f.writelines(json_issue)