import os
import glob
import hashlib
import uuid
from datetime import datetime, date
from os.path import dirname
from models.account import User, Post, Like, Follows
from PIL import Image
from models.db import DBsession
from models.db import Base
from models.account import session


def hash_it(password):
    '''
    密码加密
    :param password:
    :return:
    '''
    return hashlib.md5(password.encode('utf8')).hexdigest()


def get_user_row(user_id):
    user_info = session.query(User).filter_by(id=user_id).first()
    return user_info


def get_user_info(username):
    user_info = User.query(username)
    if user_info:
        return user_info
    else:
        return {'msg': 'register first'}


def register(username, password):
    """
    注册
    :param username:
    :param password:
    :return:
    """
    if User.is_exists(username):
        return {'msg': username}
    hash_pass = hash_it(password)
    User.add(username, hash_pass)
    return {'msg': 'ok'}


def add_post_for(username, img_url, thumb_url):
    """
    posts表增加数据
    :param username:
    :param img_url:
    :param thumb_url:
    :return:
    """
    user = User.query(username)
    post = Post(img_url=img_url, user=user, thumb_url=thumb_url)
    session.add(post)
    session.commit()
    return post


def get_post_for(username):
    """
    通过用户名获取图片地址及时间
    :param username:
    :return:
    """
    user = session.query(User).filter_by(name=username).first()
    posts = session.query(Post).order_by(Post.id.desc()).filter_by(user=user, cancel_ud=0)
    ret = []
    for p in posts:
        ret.append((p.img_url, p.created, p.id))
    return ret


def get_post_username_created(post_id):
    """
    通过id获取用户名及时间
    :param post_id:
    :return:
    """
    p = session.query(Post).filter_by(id=post_id).first()
    ret = [p.user.name, p.created]
    print(ret)
    return ret


def get_thumb_url():
    """
    通过id获取缩略图地址
    :return:
    """
    thumb_urls = session.query(Post).order_by(Post.id.desc()).filter_by(cancel_ud=0).all()
    ret = []
    for p in thumb_urls:
        ret.append((p.id, p.thumb_url))
    print(ret)
    return ret


def get_img_url(post_id):
    """通过id获取图片地址"""
    print(post_id)
    p = session.query(Post).filter_by(id=post_id).first()
    print(p)
    img_url = p.img_url
    return img_url


def add_id_for_likes(username, post_id):
    """给likes表添加数据"""
    p = session.query(User).filter_by(name=username).first()
    p1 = session.query(Post).filter_by(id=post_id).first()
    if p.id != p1.user_id:
        Like.add(user_id=p.id, post_id=post_id)
    else:
        return False


def is_exist(username, post_id):
    '''判断数据是否存在，返回True代表存在，反之不存在'''
    p = session.query(User).filter_by(name=username).first()
    user_id = p.id
    return Like.is_exist(user_id=user_id, post_id=post_id)


def drop(username, post_id):
    """删除likes表数据"""
    p = session.query(User).filter_by(name=username).first()
    Like.drop(user_id=p.id, post_id=post_id)


def get_user_like_img(username):
    """通过用户名获得用户关注图片的地址"""
    u = session.query(User).filter_by(name=username).first()
    # print(u.id)
    p = session.query(Like).filter_by(user_id=u.id).all()
    # print(p)
    ret = []
    for i in p:
        print(i.post_id)
        a = session.query(Post).filter_by(id=i.post_id).first()
        ret.append(a.img_url)
    return ret


def img_count(post_id):
    """记录图片的关注次数"""
    p = session.query(Like).filter_by(post_id=post_id).all()
    return len(p)


def get_birthday(birth):
    d = birth.split('-')
    birth = date(int(d[0]), int(d[1]), int(d[2]))
    return birth


class Upload:
    '''
    上传图片模块
    '''
    upfile_dir = 'newfile'
    thumb_dir = 'newfile_thumbnail'
    size = (200, 200)

    def __init__(self, static_path, file_name):
        '''
        初始化函数
        :param static_path: 静态文件路径
        :param file_name: 图片名
        '''
        self.static_path = static_path
        self.file_name = file_name
        self.newname = self.get_newname()

    @property
    def upload_url(self):
        return os.path.join(self.upfile_dir, self.newname)

    @property
    def upload_path(self):
        '''
        文件上传地址
        :return:
        '''
        return os.path.join(self.static_path, self.upload_url)

    def save_img(self, content):
        '''
        保存图片的操作
        :param content: 图片内容
        :return:
        '''
        with open(self.upload_path, 'wb') as f:
            f.write(content)

    def get_newname(self):
        """
        生成一个唯一的图片名
        :param filename: 上传图片的名字
        :return:
        """
        _, ext = os.path.splitext(self.file_name)
        return uuid.uuid4().hex + ext

    @property
    def thumb_url(self):
        base, _ = os.path.splitext(self.newname)
        return os.path.join(self.thumb_dir, '{}_{}x{}.jpg'.format(base, self.size[0], self.size[1]))

    @property
    def thumb_path(self):
        '''
        返回缩略图保存地址
        :return:
        '''
        return os.path.join(self.static_path, self.thumb_url, )

    def thumb(self):
        '''
        创建缩略图操作
        :return:
        '''
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        im.save(self.thumb_path, 'JPEG')
