import os
import glob
from PIL import Image
def thumb(filepath,file_n):
    im = Image.open(filepath)
    print(im.mode)
    im.thumbnail((80, 80))
    im.save('/home/pyvip/img_sharing/static/newfile_thumbnail/{}'.format(file_n[0]['filename']), 'JPEG')

user_info = {
    'username':'too',
    'passwd':'too123'
}




