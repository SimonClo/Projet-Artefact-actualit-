class RawArticle:
    """A representation of an article
    """
    def __init__(self,id_article,title,newspaper,date,url,text):
        """Create the article from the given arguments
        
        Arguments:
            title {string} -- title of the article
            newspaper {string} -- name of the newspaper the article was published in
            date {string} -- date the article was published
            url {string} -- url where the article can be found
            text {string} -- content of the article
        """
        self.id = id_article
        self.title = title
        self.text = text
        self.newspaper = newspaper
        self.date = date
        self.url = url

class SplitArticle:
    """A representation of a split article used for preprocessing
    """
    def __init__(self,id_article,title,newspaper,date,url,tokens):
        """Create the processed article from given arguments
        
        Arguments:
            title {text} -- title of the article
            newspaper {text} -- newspaper article was published n
            date {string} -- date the article was published
            url {string} -- url where the article can be found
            tokens {list(string)} -- tokens in the article
        """
        self.id = id_article 
        self.title = title
        self.newspaper = newspaper
        self.date = date
        self.url = url
        self.tokens = tokens

    def apply_to_tokens(self,function):
        """Apply a process to all tokens in article
        
        Arguments:
            function {function(token)} -- process to be applied
        """
        self.tokens = [function(token) for token in self.tokens]

class ProcessedCorpus:
    """A representation of all articles in a corpus
    """
    def __init__(self,articles):
        """Creates corpus from a list of Tokenized articles
        
        Arguments:
            articles {list(SpliArticle)} -- Split articles in the corpus
        """
        self.articles = articles

    def apply_to_articles(self,function):
        """Apply a process to all articles in corpus
        
        Arguments:
            function {function(list(token))} -- process to apply to all articles
        """
        for article in self.articles:
            article.tokens = function(article.tokens)

    def apply_to_tokens_in_articles(self,function):
        """Apply a process to all tokens of all articles from the corpus
        
        Arguments:
            function {fucntion(token)} -- process to apply to all tokens
        """
        for split_article in self.articles :
            split_article.apply_to_tokens(function)