import os
# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# static路径
STATIC_PATH = os.path.join(BASE_DIR, 'static')
# templates路径
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
DATABASE = {
    'NAME': 'flask7',
    'USER': 'root',
    'PASSWORD': '123456',
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'ENGINE': 'mysql',
    'DRIVER': 'pymysql'
}
# media路径
MEDIA_PATH = os.path.join(STATIC_PATH, 'media')