class Article:
    """A representation of an article
    """
    def __init__(self,title,newspaper,date,url,text):
        """Create the article from the given arguments
        
        Arguments:
            title {string} -- title of the article
            newspaper {string} -- name of the newspaper the article was published in
            date {string} -- date the article was published
            url {string} -- url where the article can be found
            text {string} -- content of the article
        """
        self.title = title
        self.text = text
        self.newspaper = newspaper
        self.date = date
        self.url = url