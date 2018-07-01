import tornado.web
import json
import os
import glob
import re
from tornado.web import authenticated
from pycket.session import SessionMixin
from utlis import get_birthday,register,hash_it,add_post_for,get_post_for,Upload,get_thumb_url,get_img_url,get_post_username_created,add_id_for_likes,get_user_like_img,img_count,is_exist,drop
from aid_func.account import update,get_rows_in_userdetails,get_rows_in_users,add_rows_for_userdetails,modify_info
class BaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None

class IndexHandler(BaseHandler):
    '''
    home page
    '''
    @authenticated
    def get(self, *args, **kwargs):
        # img_path = os.path.join(self.settings.get('static_path'),'newfile')
        # filepath = glob.glob('{}/*.jpg'.format(img_path))
        # print(filepath)
        img_urls = get_post_for(self.current_user)
        username = self.current_user
        self.render('index.html',filepath = img_urls,username=username,)

class ExploreHandler(BaseHandler):
    '''
    Explore page , photo of other users
    '''
    @authenticated
    def get(self, *args, **kwargs):
        thumb_urls = get_thumb_url()
        #print(filepath)
        self.render('explore.html',thumb_urls = thumb_urls)

class PostHandler(BaseHandler):
    '''
    personal page
    '''
    @authenticated
    def get(self,post_id):
        post_id = int(post_id)
        img_url = get_img_url(post_id)
        username_created = get_post_username_created(post_id)
        counts = img_count(post_id)
        result = is_exist(username=self.current_user, post_id=post_id)
        self.render('post.html',img_url = img_url,username_created=username_created,post_id=post_id,counts=counts,result=result)
    def post(self, *args, **kwargs):
        username = self.current_user
        request = self.request.full_url()
        res = re.findall(r'[0-9]+$',request)
        pos = int(res[0])
        #print(pos)
        post_id = int(pos)
        result = is_exist(username=username, post_id=post_id)
        if result==False:
            add_id_for_likes(username,post_id)
        else:
            drop(username=self.current_user, post_id=post_id)
        self.redirect('/profile')
class UploadHandler(BaseHandler):
    '''
    上传文件
    '''
    @authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')
    def post(self, *args, **kwargs):
        static_path  = self.settings.get('static_path')
        file_n = self.request.files.get('newfile',None)
        for a in file_n:
            filename = a['filename']
            saver = Upload(static_path,filename)
            saver.save_img(a['body'])
            saver.thumb()
            add_post_for(self.current_user,saver.upload_url,saver.thumb_url)
        self.write('ok')
        self.redirect('/exp')

class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        nextname = self.get_argument('next','')
        self.render('login.html',nextname = nextname)
    def post(self, *args, **kwargs):
        from utlis import get_user_info
        '''获取表单提交信息'''
        nextname = self.get_argument('next','')
        username = self.get_argument('username','')
        passwd = self.get_argument('passwd','')
        hash_pass = hash_it(passwd)
        '''验证信息'''
        if username:
            user_info = get_user_info(username)
            if user_info == { 'msg':'register first'}:
                self.write(user_info)
            else:
                if username == user_info.name and hash_pass == user_info.password:
                    self.session.set('user',username)
                    if nextname:
                        self.redirect(nextname)
                    else:
                        self.redirect('/')
                else:
                    self.write('账号或密码错误')
        else:
            self.write('账号或密码错误')

class LogoutHandler(BaseHandler):
    def get(self):
        nextname = self.get_argument('next', '')
        self.session.set('user','')
        self.render('login.html',nextname=nextname)

class RegisterHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render('register.html',msg ='')

    def post(self, *args, **kwargs):
        from datetime import datetime,date
        username = self.get_argument('username','')
        passwd1 = self.get_argument('passwd1','')
        passwd2 = self.get_argument('passwd2','')
        #email = self.get_argument('email','')
        if username and passwd1 and passwd2:
            if passwd1 != passwd2:
                self.write('两次输入的密码不一致')
            else:
                ret = register(username,passwd1)
                if ret['msg'] =='ok':
                    self.session.set('user',username)
                    birth = date(2018,1,1)
                    add_rows_for_userdetails(username=self.current_user, email='', phone='', birth=birth, gender=1,introduce='lazy')
                    self.redirect('/')
                else:
                    self.write(ret)
        else:
            self.render('register.html',msg={'register':'fail'})

class ProfileHandler(BaseHandler):
    def get(self):
        img_urls = get_post_for(self.current_user)
        username = self.current_user
        img_urls_list = get_user_like_img(username)
        self.render('profile.html',filepath=img_urls, username=username,img_urls=img_urls_list)
    def post(self, *args, **kwargs):
        post_id = self.get_arguments('post_id')
        update(post_id)
        self.redirect('/profile')
class InformationHandler(BaseHandler):
    @authenticated
    def get(self):
        username = self.current_user
        ud_row = get_rows_in_userdetails(username)
        if ud_row.gender:
            gender = '男'
        else:
            gender = '女'
        self.render('per_information.html',username=username,email=ud_row.email,phone=ud_row.phone,gender=gender,introduce=ud_row.introduce,birth=ud_row.birth)
        #self.render('input_info.html')

    def post(self, *args, **kwargs):
        email =self.get_argument('email','')
        phone = self.get_argument('phone','')
        birth = self.get_argument('birth','')
        gender = self.get_argument('customRadio','')
        introduce = self.get_argument('introduce','')
        #print(email,phone,birth,gender,introudce)
        add_rows_for_userdetails(username=self.current_user,email=email,phone=phone,birth=birth,gender=int(gender),introduce=introduce)
        self.redirect('/info')
class ModifyHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('input_info.html')
    def post(self, *args, **kwargs):
        ud_row = get_rows_in_userdetails(self.current_user)
        email = self.get_argument('email', ud_row.email)
        phone = self.get_argument('phone', ud_row.phone)
        birth = self.get_argument('birth', ud_row.birth)
        birth = get_birthday(birth)
        gender = self.get_argument('customRadio', ud_row.gender)
        introduce = self.get_argument('introduce', ud_row.introduce)
        print(birth,gender)
        modify_info(username=self.current_user,email=email,phone=phone,birth=birth,gender=int(gender),introduce=introduce)
        self.redirect('/info')

class TestajaxHandler(BaseHandler):
    def get(self):
        self.render('test.html')
    def post(self):
        a = self.get_argument('a','')
        b = self.get_argument('b','')
        resp = """Content-Type: text/json;charset=GBK
                {"name":"xiaopo","age":"18"}
            """
        print(a,b)
