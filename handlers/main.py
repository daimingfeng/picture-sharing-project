import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    '''
    home page
    '''
    def get(self, *args, **kwargs):
        self.render('index.html')

class ExploreHandler(tornado.web.RequestHandler):
    '''
    Explore page , photo of other users
    '''
    def get(self, *args, **kwargs):
        self.render('explore.html')

class PostHandler(tornado.web.RequestHandler):
    '''
    personal page
    '''
    def get(self,post_id):
            self.render('post.html',post_id = post_id)