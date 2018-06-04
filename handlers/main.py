import tornado.web
import os
import glob
from PIL import Image
class IndexHandler(tornado.web.RequestHandler):
    '''
    home page
    '''
    def get(self, *args, **kwargs):
        img_path = os.path.join(self.settings.get('static_path'),'newfile')
        filepath = glob.glob('{}/*.jpg'.format(img_path))
        print(filepath)
        self.render('index.html',filepath = filepath)

class ExploreHandler(tornado.web.RequestHandler):
    '''
    Explore page , photo of other users
    '''
    def get(self, *args, **kwargs):
        img_path = os.path.join(self.settings.get('static_path'),'newfile_thumbnail')
        filepath = glob.glob('{}/*.jpg'.format(img_path))
        print(filepath)
        self.render('explore.html',filepath = filepath)

class PostHandler(tornado.web.RequestHandler):
    '''
    personal page
    '''
    def get(self,post_name):
            self.render('post.html',post_name = post_name)

class UploadHandler(tornado.web.RequestHandler):
    '''
    上传文件
    '''
    def get(self, *args, **kwargs):
        self.render('upload.html')
    def post(self, *args, **kwargs):
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
        im = Image.open(filepath)
        print(im.mode)
        im.thumbnail((80,80))
        im.save('/home/pyvip/img_sharing/static/newfile_thumbnail/{}'.format(file_n[0]['filename']),'JPEG')
        self.write('ok')