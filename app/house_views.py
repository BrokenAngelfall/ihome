import datetime
import os

from flask import Blueprint, session, render_template, request, jsonify

from app.models import User, House, Area, Facility, db, HouseImage, Order
from untils import status_code
from untils.functions import login_check
from untils.settings import MEDIA_PATH

blue_house = Blueprint('house', __name__)


@blue_house.route('/my_house/', methods=['GET'])
@login_check
def my_house():
    if request.method == 'GET':
        return render_template('myhouse.html')


@blue_house.route('/i_house/', methods=['POST', 'GET'])
def i_house():
    if request.method == 'GET':
        id = session.get('user_id')
        user = User.query.filter(User.id == id).first()
        name = user.id_name
        id_card = user.id_card
        ihome_house = House.query.filter(House.user_id == id).all()
        house_info = [house.to_dict() for house in ihome_house]

        return jsonify({'name': name, 'id_card': id_card, 'house_info': house_info})


@blue_house.route('/new_house/', methods=['GET', 'POST'])
@login_check
def new_house():
    if request.method == 'GET':
        return render_template('newhouse.html')
    if request.method == 'POST':
        checked_id = request.form.getlist('facility')
        title = request.form.get('title')
        price = request.form.get('price')
        area_id = request.form.get('area_id')
        address = request.form.get('address')
        room_count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        house = House()
        house.title = title
        house.price = price
        house.address = address
        house.user_id = session.get('user_id')
        house.area_id = area_id
        house.beds = beds
        house.max_days = max_days
        house.min_days = min_days
        house.deposit = deposit
        house.unit = unit
        house.room_count = room_count
        house.acreage = acreage
        db.session.add(house)
        db.session.commit()
        for i in checked_id:
            facility = Facility.query.filter(Facility.id == int(i)).first()
            house.facilities.append(facility)
        db.session.commit()
        id = house.id
        return jsonify({'code': 200, 'id': id})


@blue_house.route('/house_address/')
def house_address():
    if request.method == 'GET':
        areas = Area.query.all()
        address = [area.to_dict() for area in areas]
        return jsonify({'address': address})


@blue_house.route('/img/', methods=['GET', 'POST'])
def img():
    if request.method == 'POST':
        img = request.files.get('house_image')
        id = request.form.get('house_id')
        house_img = HouseImage()
        house = House.query.filter(House.id == id)
        path = os.path.join(MEDIA_PATH, img.filename)
        img.save(path)
        house_img.url = img.filename
        house_img.house_id = id
        house.index_image_url = img.filename
        db.session.add(house)
        db.session.commit()
        db.session.add(house_img)
        db.session.commit()

        return jsonify(status_code.OK)


@blue_house.route('/detail/', methods=['POST', 'GET'])
def detail():
    if request.method == 'GET':
        return render_template('detail.html')


@blue_house.route('/detail/<int:id>/', methods=['POST', 'GET'])
def detail_id(id):
    if request.method == 'GET':
        booking = 1
        house = House.query.get(id)
        house_facilities = house.facilities
        house1 = house.to_full_dict()
        name = []
        for i in house_facilities:
            name.append(i.name)
        user_id = session.get('user_id')
        if house.user_id == user_id:
            booking =0
        return jsonify(code=status_code.OK, house=house1, name=name, booking=booking)


@blue_house.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')


@blue_house.route('/search_house/',methods=['GET', 'POST'])
def search_house():
    if request.method == 'GET':
        user_id = session['user_id']
        address = request.args.get('address')
        begin_date = request.args.get('begin_date')
        end_date = request.args.get('end_date')
        order_by = request.args.get('order_by')
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        days = end_date - begin_date
        house_list = House.query.filter(House.max_days >= days,
                                        House.min_days <= days,
                                        House.address == address and House.user_id != user_id
                                        )
        order1 = Order.query.filter(Order.begin_date > end_date).all()
        order2 = Order.query.filter(Order.end_date < begin_date).all()
        order3 = order2+order1

        if not house_list and not order3:
            return jsonify(code=1008, msg='没有房间')

        house_now = house_list.query.filter(House.id.in_(order.house_id for order in order3)).order_by(house_list.id).all()
        if house_now:
            house_show = [house for house in house_now]
            return jsonify(code=status_code.OK, house_shouw=house_show)


