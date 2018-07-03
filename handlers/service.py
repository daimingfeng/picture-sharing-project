import time
import uuid
from datetime import datetime
import tornado.httpclient
import tornado.web
import tornado.gen
import tornado.escape
from .main import BaseHandler
from utlis import Upload, add_post_for
from .chat import ChatSocketHandler


class ImageSaveHandler(BaseHandler):
    """
    异步图片保存
    """

    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        print(self.request.remote_ip == "::1")
        is_room = self.get_arguments('room') == 'room'
        url = self.get_arguments('url')
        username = self.get_arguments('user')

        if not (username and is_room):
            print('no user and room')
            return
        resp = yield self.fetch_img(url)
        if not resp.body:
            self.write('data empty')
            return
        img_saver = Upload(self.settings.get('static_path'), 'x.jpg')
        img_saver.save_img(resp.body)
        img_saver.thumb()

        post = add_post_for(username, img_saver.upload_url, img_saver.thumb_url)
        chat = {
            "id": str(uuid.uuid4()),
            "username": '--admin',
            "body": '{} post:{}'.format(username, 'http://192.168.152.128:8001/post/{}'.format(post.id)),
            "img": post.thumb_url,
        }
        chat["html"] = tornado.escape.to_basestring(self.render_string("message.html", message=chat))
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)
        print('message sent!')
        self.redirect('/post/{}'.format(post.id))

    @tornado.gen.coroutine
    def fetch_img(self, url):
        """
        内部模拟浏览器，下载图片
        :return:
        """
        url = self.get_argument('url', None)
        client = tornado.httpclient.AsyncHTTPClient()
        print('-- {} -- going to fetch {}'.format(datetime.now(), url))
        resp = yield client.fetch(url)
        return resp
