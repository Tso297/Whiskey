from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, car_schema, cars_schema, Car_Dealership

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return ('yee: haw')

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car_Dealership(name, email, phone_number, address, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car_Dealership.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car_Dealership.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car_Dealership.query.get(id)
    car.name = request.json['name']
    car.email = request.json['email']
    car.phone_number = request.json['phone_number']
    car.address = request.json['address']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car_Dealership.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)