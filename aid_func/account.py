import os
import glob
import hashlib
import uuid
from os.path import dirname
from models.account import User,Post,Like,Userdetails
from PIL import Image
from models.db import DBsession
from models.db import Base
from models.account import session
def get_rows_in_users(username):
    """获取users表中行"""
    row = session.query(User).filter_by(name=username).first()
    return row
def add_rows_for_userdetails(username,email,phone,birth,gender,introduce):
    """添加数据到usersdetails表中"""
    row = get_rows_in_users(username)
    print(row)
    Userdetails.add(user_id=row.id,email=email,phone=phone,birth=birth,gender=gender,introduce=introduce)

def get_rows_in_userdetails(username):
    """获取userdetails表中行"""
    ud_row = get_rows_in_users(username)
    row = session.query(Userdetails).filter_by(user_id=ud_row.id).first()
    return row

def modify_info(username,email,phone,birth,gender,introduce):
    """跟新userdetails表中数据"""
    row = get_rows_in_users(username)
    Userdetails.update(user_id=row.id,email=email,phone=phone,birth=birth,gender=gender,introduce=introduce)

def update(post_id):
    """跟新posts表中数据，标记为用户取消上传的图片"""
    Post.update(post_id)

