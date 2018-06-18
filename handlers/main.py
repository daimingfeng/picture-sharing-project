import tornado.web
import os
import glob
from tornado.web import authenticated
from pycket.session import SessionMixin
from utlis import register,hash_it,add_post_for,get_post_for,Upload
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
        self.render('index.html',filepath = img_urls)

class ExploreHandler(BaseHandler):
    '''
    Explore page , photo of other users
    '''
    @authenticated
    def get(self, *args, **kwargs):
        img_path = os.path.join(self.settings.get('static_path'),'newfile_thumbnail')
        filepath = glob.glob('{}/*.jpg'.format(img_path))
        #print(filepath)
        self.render('explore.html',filepath = filepath)

class PostHandler(BaseHandler):
    '''
    personal page
    '''
    @authenticated
    def get(self,post_name):
            self.render('post.html',post_name = post_name)

class UploadHandler(BaseHandler):
    '''
    上传文件
    '''
    @authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')
    def post(self, *args, **kwargs):
        from utlis import thumb
        static_path  = self.settings.get('static_path')
        #print(upload_dir_path)
        file_n = self.request.files.get('newfile',None)
        #print(file_n)
        for a in file_n:
            filename = a['filename']
            saver = Upload(static_path,filename)
            #print(filename)
            saver.save_img(a['body'])
            # filepath = os.path.join(self.settings.get('static_path'),'newfile',filename)
            # print(filepath)
            # with open(filepath,'wb') as f:
            #     f.write(a['body'])
            add_post_for(self.current_user,saver.upload_path)
            saver.thumb()
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
            if username == user_info.name and hash_pass == user_info.password:
                self.session.set('user',username)
                #print(nextname)
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
        self.session.set('user','')
        self.render('login.html')

class RegisterHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render('register.html',msg ='')

    def post(self, *args, **kwargs):
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
                    self.redirect('/')
                else:
                    self.write(ret)
        else:
            self.render('register.html',msg={'register':'fail'})

