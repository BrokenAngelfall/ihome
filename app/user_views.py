import os
import re

from flask import Blueprint, request, render_template, jsonify, session, g
from werkzeug.security import check_password_hash

from app.models import User, db

from untils import status_code
from untils.functions import random_str, login_check
from untils.settings import MEDIA_PATH, BASE_DIR

blue = Blueprint('user', __name__)


@blue.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':

        return render_template('register.html')

    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        password1 = request.form.get('password2')
        str1 = request.form.get('str1')
        imagecode = request.form.get('imagecode')
        regex = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
        if not re.match(regex, mobile):
            return jsonify(status_code.USER_REGISTER_MOBILE)
        if password != password1:
            return jsonify(status_code.USER_REGISTER_PASSWORD)
        user = User.query.filter(User.phone == mobile).first()
        if user:
            return jsonify(status_code.USER_REGISTER_MOBILE_EXIST)
        if str1 != imagecode:
            return jsonify(status_code.USER_REGISTER_CODE)
        user = User()
        user.phone = mobile
        g.mobile = mobile
        user.password = password
        db.session.add(user)
        db.session.commit()
        return jsonify(status_code.USER_REGISTER_SUCCEED)


@blue.route('/register_code/', methods=['GET'])
def register_code():
    if request.method == 'GET':
        str1 = random_str()
        return jsonify({'str1': str1})


@blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')

        user =User.query.filter(User.phone == mobile).first()
        if user.phone == mobile and check_password_hash(user.pwd_hash, password):
            session['user_id'] = user.id
            return jsonify(status_code.USER_REGISTER_SUCCEED)
        else:
            return jsonify(status_code.USER_REGISTER_MOBILE_PASSWORD_ERROR)


@blue.route('/my/', methods=['GET', 'POST'])
@login_check
def my():
    if request.method == 'GET':
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        name = user.name
        phone = user.phone
        src = user.avatar
        return render_template('my.html', name=name, phone=phone, src1=src)


@blue.route('/profile/', methods=['GET', 'POST', 'PATCH'])
@login_check
def profile():
    user_id = session['user_id']
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'PATCH':
        avatar = request.files.get('avatar')
        if avatar:
            user = User.query.filter(User.id == user_id).first()
            path = os.path.join(MEDIA_PATH, avatar.filename)
            user.avatar = avatar.filename
            avatar.save(path)
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '上传成功', 'path': user.avatar})
        else:
            return jsonify(status_code.USER_REGISTER_AVATAR_ERROR)


@blue.route('/name/', methods=['PATCH'])
def name():
    if request.method == 'PATCH':
        name = request.form.get('name')
        id = session['user_id']
        user = User.query.filter(User.id == id).first()
        user.name = name
        db.session.add(user)
        db.session.commit()
        return jsonify(status_code.OK)


@blue.route('/auth/', methods=['GET', 'POST'])
@login_check
def auth():
    if request.method == 'GET':
        id = session['user_id']
        user = User.query.filter(User.id == id).first()
        name = user.id_name
        id_card = user.id_card
        return render_template('auth.html', name=name, id_card=id_card)
    if request.method == 'POST':
        name = request.form.get('name')
        id_card = request.form.get('id_card')
        reg = r"^[\u4E00-\u9FA5\uf900-\ufa2d]{2,20}$"
        if not re.match(reg, name):
            return jsonify(status_code.NAME_ERROR)
        reg_id =r"(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)"
        if not re.match(reg_id, id_card):
            return jsonify(status_code.ID_CARD_ERROR)
        user_card = User.query.filter(User.id_card == id_card).first()
        if user_card:
            return jsonify(status_code.ID_CARD_EXIST)
        id = session.get('user_id')
        user = User.query.filter(User.id == id).first()
        user.id_card = id_card
        user.id_name = name
        db.session.add(user)
        db.session.commit()
        return jsonify(status_code.OK)


@blue.route('/logout/', methods=['POST', 'GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return render_template('login.html')