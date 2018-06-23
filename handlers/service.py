import time
from datetime import datetime
import tornado.httpclient
import tornado.web
import tornado.gen
from .main import BaseHandler
from utlis import Upload,add_post_for

class ImageSaveHandler(BaseHandler):
    """
    异步图片保存
    """
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        resp = yield self.fetch_img()
        print(resp)
        if not resp.body:
            self.write('data empty')
            return
        img_saver = Upload(self.settings.get('static_path'),'x.jpg')
        print(resp.body)
        img_saver.save_img(resp.body)
        img_saver.thumb()
        post = add_post_for(self.current_user,img_saver.upload_url,img_saver.thumb_url)
        self.redirect('/post/{}'.format(post.id))


    def fetch_img(self):
        """
        内部模拟浏览器，下载图片
        :return:
        """
        url = self.get_argument('url',None)
        client = tornado.httpclient.AsyncHTTPClient()
        print('-- {} -- going to fetch {}'.format(datetime.now(),url))

        return client.fetch(url)