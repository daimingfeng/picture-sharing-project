import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define,options
from handlers import main
define('port',default=8000,help='run port',type=int)
define('version',default='0.0.1',help='version0.0.1',type=str)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/',main.IndexHandler),
            (r'/exp',main.ExploreHandler),
            (r'/post/(?P<post_name>.*)',main.PostHandler),
            (r'/upload',main.UploadHandler),
        ]
        settings = dict(
            template_path = 'templates',
            static_path = 'static',
            debug = True,
            )

        super(Application,self).__init__(handlers,**settings)

application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print('Sever start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()