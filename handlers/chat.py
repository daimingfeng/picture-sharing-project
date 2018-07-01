import logging
import re
import tornado.escape
import tornado.web
import tornado.websocket
import uuid
from .main import BaseHandler
from tornado.web import authenticated
class RoomHandler(BaseHandler):
    """
    聊天室
    """
    @authenticated
    def get(self):
        self.render('room.html',messages=ChatSocketHandler.cache)

class ChatSocketHandler(tornado.websocket.WebSocketHandler,BaseHandler):
    waiters = set()      # 等待接收消息的用户
    cache = []           # 存放消息
    cache_size = 200     # 消息列表的大小

    def get_compression_options(self):
        """
        非None的返回值开启压缩
        :return:
        """
        return {}

    def open(self):
        """
        新的WebSocke连接打开
        :return:
        """
        logging.info("new connection %s"%self)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        """
        WebSocket连接断开
        :return:
        """
        return ChatSocketHandler.waiters.remove(self)
    @classmethod
    def update_cache(cls,chat):
        """
        跟新消息列表，加入新的消息
        :param chat:
        :return:
        """
        cls.\
            cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls,chat):
        """
        给每个等待接收的用户发新的消息
        :param chat:
        :return:
        """
        logging.info("sending message to %d waiters",len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message",exc_info=True)
    def on_message(self, message):
        """WebSocket 服务器端接收到消息"""
        logging.info("got message %r",message)
        parsed = tornado.escape.json_decode(message)
        if parsed["body"] == '':
            return
        if re.findall(r'^http://.*.jpg$',parsed["body"]) != []:
            img_url = 'http://127.0.0.1:8000/save?url={}&from=room&user={}'.format(parsed["body"],self.current_user)
            from tornado.httpclient import AsyncHTTPClient
            from tornado.ioloop import IOLoop
            c = AsyncHTTPClient()
            IOLoop.current().spawn_callback(c.fetch,img_url)
            chat = {
                "id":str(uuid.uuid4()),
                "username":'--admin',
                "body":'{},url is processsing:{}'.format(self.current_user,parsed["body"]),
                "img":None,
            }
            chat["html"] = tornado.escape.to_basestring(self.render_string("message.html", message=chat))
            self.write_message(chat)
        else:
            chat = {
                "id":str(uuid.uuid4()),
                "body": parsed["body"],
                'username':'--{}'.format(self.current_user),
                "img":None,
            }
            chat["html"] = tornado.escape.to_basestring(self.render_string("message.html",message=chat))
            ChatSocketHandler.update_cache(chat)
            ChatSocketHandler.send_updates(chat)
