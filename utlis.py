import os
import glob
import hashlib
from os.path import dirname
from models.account import User,Post
from PIL import Image
from models.db import DBsession
from models.db import Base
from models.account import session
def thumb(filepath,upload_dir_path):
    dirname = os.path.dirname(filepath)
    file,ext = os.path.splitext(os.path.basename(filepath))
    im = Image.open(filepath)
    size =(200,200)
    im.thumbnail(size)
    save_thumb_to = os.path.join(upload_dir_path,'newfile_thumbnail','{}_{}x{}.jpg'.format(file,*size))
    im.save(save_thumb_to,'JPEG')


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



