import tornado.web
import tornado.ioloop
import tornado.options
from pycket.session import SessionMixin
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
            (r'/logout', main.LogoutHandler),
            (r'/login',main.LoginHandler),
            (r'/register',main.RegisterHandler),

        ]
        settings = dict(
            template_path = 'templates',
            static_path = 'static',
            login_url = '/login',
            cookie_secret = 'daimingfeng',
            debug = True,
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    'db_sessions': 5,
                    'db_notifications': 11,
                    'max_connections': 2 ** 31,
                },
                'cookies': {
                    'expires_days': 60,
                    'max_age': 100,
                }
            }
            )


        super(Application,self).__init__(handlers,**settings)

application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print('Sever start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()