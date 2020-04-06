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

class Match:

    def __init__(self, id_archive, id_recent_article, score):
        self.id_archive = id_archive
        self.id_recent_article = id_recent_article
        self.score = score