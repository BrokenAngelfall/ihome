
from flask import Blueprint, request, render_template, session, jsonify

from app.models import Order, User, db, Area
from untils import status_code

blue_order = Blueprint('order', __name__)


@blue_order.route('/lorder/', methods=['GET', 'POST'])
def lorder():
    if request.method == 'GET':
        return render_template('lorders.html')


@blue_order.route('/my_order/', methods=['GET', 'POST'])
def my_order():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        orders = user.orders
        orders = [order.to_dict() for order in orders]
        return jsonify(code=status_code.OK, order=orders)


@blue_order.route('/orders/', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        return render_template('orders.html')


@blue_order.route('/my_orders/', methods=['GET', 'POST'])
def my_orders():
    if request.method == 'GET':
        user_id = session.get('user_id')
        orders = Order.query.filter(Order.user_id == user_id).all()
        orders = [order.to_dict() for order in orders]
        return jsonify(code=status_code.OK, order=orders)


@blue_order.route('/evaluate/', methods=['POST', 'GET'])
def evaluate():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        content = request.form.get('content')
        order = Order.query.filter(Order.id == order_id).first()
        order.comment = content
        db.session.add(order)
        db.session.commit()
        return None


@blue_order.route('/index/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':

        return render_template('index.html')


@blue_order.route('/index_name/', methods=['POST', 'GET'])
def index_name():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        name = user.name
        areas = Area.query.all()
        areas = [area.to_dict() for area in areas]
        return jsonify(code=status_code.OK, name=name, areas=areas)

