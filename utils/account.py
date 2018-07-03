import os
import glob
import hashlib
import uuid
from os.path import dirname
from models.account import User, Post, Like, Userdetails, Follows
from PIL import Image
from models.db import DBsession
from models.db import Base
from models.account import session
from utlis import get_user_row

"""users"""


def get_rows_in_users(username):
    """获取users表中行"""
    row = session.query(User).filter_by(name=username).first()
    return row


"""posts"""


def update(post_id):
    """跟新posts表中数据，标记为用户取消上传的图片"""
    Post.update(post_id)


"""userdetails"""


def add_rows_for_userdetails(username, email, phone, birth, gender, introduce):
    """添加数据到usersdetails表中"""
    row = get_rows_in_users(username)
    print(row)
    Userdetails.add(user_id=row.id, email=email, phone=phone, birth=birth, gender=gender, introduce=introduce)


def get_rows_in_userdetails(username):
    """获取userdetails表中行"""
    ud_row = get_rows_in_users(username)
    row = session.query(Userdetails).filter_by(user_id=ud_row.id).first()
    return row


def modify_info(username, email, phone, birth, gender, introduce):
    """跟新userdetails表中数据"""
    row = get_rows_in_users(username)
    Userdetails.update(user_id=row.id, email=email, phone=phone, birth=birth, gender=gender, introduce=introduce)


"""follows"""


def add_rows_for_follows(user_id, follow_id):
    """给关注表添加数据"""
    Follows.add(user_id=user_id, follow_id=follow_id)


def drop_rows_for_follows(user_id, follow_id):
    """取消关注"""
    Follows.drop(user_id=user_id, follow_id=follow_id)


def query_rows_in_follows(user_id):
    """查询follows表数据"""
    rows = session.query(Follows).filter_by(user_id=user_id).all()
    return rows


def judge_attention(current_user, username):
    """判断该用户是否已关注"""
    user_row = get_rows_in_users(username=current_user)
    follow_row = get_rows_in_users(username=username)
    rows = query_rows_in_follows(user_row.id)
    if user_row.id == follow_row.id:
        result = ('2',)
        return result
    for row in rows:
        if row.follow_id == follow_row.id:
            result = ('1', user_row, follow_row)
            return result
    result = ('0', user_row, follow_row)
    return result


def func(current_user):
    """返回用户关注对象的名字"""
    users_row = get_rows_in_users(username=current_user)
    follows_rows = query_rows_in_follows(user_id=users_row.id)
    ret = []
    for i in follows_rows:
        user_row = get_user_row(user_id=i.follow_id)
        ret.append(user_row.name)
    print(ret)
    return ret
