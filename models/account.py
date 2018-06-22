from datetime import datetime
from sqlalchemy import (Column,Integer,String,DateTime,ForeignKey)
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship
from .db import DBsession
from .db import Base
session = DBsession()
class  User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50),unique=True,nullable=False)
    password = Column(String(50),nullable=False)
    created = Column(DateTime,default=datetime.now)
    def __repr__(self):
        return '<User(#{}:{})>'.format(self.id,self.name)
    @classmethod
    def query(cls,username):
        user = session.query(cls).filter_by(name=username).first()
        if user:
            return user
        else:
            return ''

    @classmethod
    def is_exists(cls,username):
        return session.query(exists().where(User.name == username)).scalar()
    @classmethod
    def add(cls,name,hash_pw):
        user_info = User(name=name,password=hash_pw)
        session.add(user_info)
        session.commit()
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,autoincrement=True)
    img_url = Column(String(80))
    user_id = Column(Integer,ForeignKey('users.id'))
    thumb_url = Column(String(80))
    created = Column(DateTime, default=datetime.now)
    user = relationship('User',backref = 'post',uselist=False,cascade='all')


    def __repr__(self):
        return "<post(#){}>".format(self.id)
    @classmethod
    def add(cls,user,img_url,thumb_url):
        img_info = Post(user=user,img_url=img_url,thumb_url=thumb_url)
        session.add(img_info)
        session.commit()


if __name__ == '__main__':
    Base.metadata.create_all()