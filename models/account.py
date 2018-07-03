from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Boolean, Date)
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship
from .db import DBsession
from .db import Base

session = DBsession()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return '<User(#{}:{})>'.format(self.id, self.name)

    @classmethod
    def query(cls, username):
        user = session.query(cls).filter_by(name=username).first()
        if user:
            return user
        else:
            return ''

    @classmethod
    def is_exists(cls, username):
        return session.query(exists().where(User.name == username)).scalar()

    @classmethod
    def add(cls, name, hash_pw):
        user_info = User(name=name, password=hash_pw)
        session.add(user_info)
        session.commit()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_url = Column(String(80))
    user_id = Column(Integer, ForeignKey('users.id'))
    thumb_url = Column(String(80))
    created = Column(DateTime, default=datetime.now)
    cancel_ud = Column(Integer, default=0)
    user = relationship('User', backref='post', uselist=False, cascade='all')

    def __repr__(self):
        return "<post(#){}>".format(self.id)

    @classmethod
    def add(cls, user, img_url, thumb_url):
        img_info = Post(user=user, img_url=img_url, thumb_url=thumb_url)
        session.add(img_info)
        session.commit()

    @classmethod
    def update(cls, post_id):
        session.query(Post).filter_by(id=post_id).update({Post.cancel_ud: 1})
        session.commit()


class Like(Base):
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)

    def __repr__(self):
        return '<like(#) user_id:{} post_id:{}>'.format(self.user_id, self.post_id)

    @classmethod
    def is_exist(cls, user_id, post_id):
        """判断数据是否存在（用户是否已关注，返回True就是已关注）"""
        p = session.query(Like).filter_by(user_id=user_id).all()
        for i in p:
            if i.post_id == post_id:
                return True
        return False

    @classmethod
    def add(cls, user_id, post_id):
        likes_info = Like(user_id=user_id, post_id=post_id)
        session.add(likes_info)
        session.commit()

    @classmethod
    def drop(cls, user_id, post_id):
        rows = session.query(Like).filter_by(user_id=user_id, post_id=post_id).first()
        session.delete(rows)
        session.commit()


class Userdetails(Base):
    __tablename__ = 'userdetails'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    gender = Column(Boolean, default=1)
    phone = Column(String(11), default='')
    email = Column(String(50), default='')
    birth = Column(Date, nullable=True)
    introduce = Column(String(100), default='本人很懒，什么都没有留下')

    def __repr__(self):
        return '<userdetails(#) user_id:{}>'.format(self.user_id)

    @classmethod
    def add(cls, user_id, gender, phone, email, birth, introduce):
        details_info = Userdetails(user_id=user_id, gender=gender, phone=phone, email=email, birth=birth,
                                   introduce=introduce)
        session.add(details_info)
        session.commit()

    @classmethod
    def update(cls, user_id, gender, phone, email, birth, introduce):
        session.query(Userdetails).filter_by(user_id=user_id).update({Userdetails.gender: gender,
                                                                      Userdetails.phone: phone,
                                                                      Userdetails.email: email,
                                                                      Userdetails.birth: birth,
                                                                      Userdetails.introduce: introduce})
        session.commit()


class Follows(Base):
    __tablename__ = 'follows'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    follow_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return '<follows> user_id:{} follow_id:{}'.format(self.user_id, self.follow_id)

    @classmethod
    def add(cls, user_id, follow_id):
        follows_row = Follows(user_id=user_id, follow_id=follow_id)
        session.add(follows_row)
        session.commit()

    @classmethod
    def drop(cls, user_id, follow_id):
        follows_row = session.query(Follows).filter_by(user_id=user_id, follow_id=follow_id).first()
        session.delete(follows_row)
        session.commit()


if __name__ == '__main__':
    Base.metadata.create_all()
