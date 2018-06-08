import tornado.web
import os
import glob
from tornado.web import authenticated
#from pycket import session
from pycket.session import SessionMixin
from PIL import Image
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
        img_path = os.path.join(self.settings.get('static_path'),'newfile')
        filepath = glob.glob('{}/*.jpg'.format(img_path))
        print(filepath)
        self.render('index.html',filepath = filepath)

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
    def get(self,post_name):
            self.render('post.html',post_name = post_name)

class UploadHandler(BaseHandler):
    '''
    上传文件
    '''
    def get(self, *args, **kwargs):
        self.render('upload.html')
    def post(self, *args, **kwargs):
        from utlis import thumb
        upload_path = os.path.join(os.path.dirname(__file__),'newfile') # 文件暂存的路径
        print(upload_path)
        file_n = self.request.files['newfile']
        print(file_n[0]['filename'])# 提取表单中'name'为'newfile'的文件数据
        for a in file_n:
            filename = a['filename']
            print(filename)
            filepath = os.path.join('/home/pyvip/img_sharing/static/newfile',filename)
            with open(filepath,'wb') as f:
                f.write(a['body'])
        thumb(filepath,file_n)
        self.write('ok')
class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        nextname = self.get_argument('next','')
        self.render('login.html',nextname = nextname)
    def post(self, *args, **kwargs):
        from utlis import user_info
        '''获取表单提交信息'''
        nextname = self.get_argument('next','')
        username = self.get_argument('username','')
        passwd = self.get_argument('passwd','')
        '''验证信息'''
        if username:
            if username == user_info['username'] and passwd == user_info['passwd']:
                self.session.set('user',username)
                print(nextname)
                self.redirect(nextname)
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
        self.render('register.html')

    def post(self, *args, **kwargs):
        from utlis import user_info
        username = self.get_argument('username','')
        passwd1 = self.get_argument('passwd1','')
        passwd2 = self.get_argument('passwd2','')
        email = self.get_argument('email','')
        if username and passwd1 and passwd2:
            if passwd1 != passwd2:
                self.write('两次输入的密码不一致')
            else:
                pass

