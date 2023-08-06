from . import base_poster

class Poster_Article(base_poster.Base_Poster):
    def __init__(self, interface='http://121.40.187.51:8088/api/article_get'):
        self.interface = interface