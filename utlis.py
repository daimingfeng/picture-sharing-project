import os
import glob
import hashlib
from os.path import dirname
from models.account import User,Post
from PIL import Image
from models.db import DBsession
from models.db import Base
from models.account import session

def hash_it(password):
    return hashlib.md5(password.encode('utf8')).hexdigest()

def get_user_info(username):
    user_info = User.query(username)
    return user_info


def register(username,password):
    if User.is_exists(username):
        return {'msg':username}
    hash_pass = hash_it(password)
    User.add(username,hash_pass)
    return {'msg':'ok'}

def add_post_for(username,img_url):
    user = User.query(username)
    Post.add(img_url=img_url,user=user)

def get_post_for(username):
        user = session.query(User).filter_by(name=username).first()
        posts =session.query(Post).filter_by(user=user)
        ret =[]
        for p in posts:
            ret.append(p.img_url)
        return ret

class Upload:
    '''
    上传图片模块
    '''
    upfile_dir = 'newfile'
    thumb_dir = 'newfile_thumbnail'
    size = (200,200)
    def __init__(self, static_path, file_name):
        '''
        初始化函数
        :param static_path: 静态文件路径
        :param file_name: 图片名
        '''
        self.static_path = static_path
        self.file_name = file_name
    @property
    def upload_url(self):
        return os.path.join(self.upfile_dir,self.file_name)
    @property
    def upload_path(self):
        '''
        文件上传地址
        :return:
        '''
        return os.path.join(self.static_path,self.upload_url)
    def save_img(self,content):
        '''
        保存图片的操作
        :param content: 图片内容
        :return:
        '''
        with open(self.upload_path,'wb') as f:
            f.write(content)
    @property
    def thumb_path(self):
        '''
        返回缩略图保存地址
        :return:
        '''
        base,_ = os.path.splitext(self.file_name)
        return os.path.join(self.static_path,self.thumb_dir,'{}_{}x{}.jpg'.format(base,self.size[0],self.size[1]))
    def thumb(self):
        '''
        创建缩略图操作
        :return:
        '''
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        im.save(self.thumb_path,'JPEG')



