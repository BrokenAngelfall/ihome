import os

from flask import Flask
from flask_script import Manager

from app.house_views import blue_house
from app.models import db
from app.order_views import blue_order
from app.user_views import blue
from untils.settings import STATIC_PATH, TEMPLATE_PATH

app = Flask(__name__,
            static_folder=STATIC_PATH,
            template_folder=TEMPLATE_PATH
            )

app.register_blueprint(blueprint=blue, url_prefix='/user/')
app.register_blueprint(blueprint=blue_house, url_prefix='/house/')
app.register_blueprint(blueprint=blue_order, url_prefix='/order/')
# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/ihome'
app.config['SQLALCHEMY_TRACK_MODIFICATTIONS'] = False
app.config['SECRET_KEY'] = '111'
# 初始化db和app对象
db.init_app(app)
# 配置文件路径


manage = Manager(app)
if __name__ == '__main__':
    manage.run()