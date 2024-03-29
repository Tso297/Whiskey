from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, whiskey_schema, whiskeys_schema, Whiskey_Collection

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/whiskeys', methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    whiskey = request.json['whiskey']
    origin = request.json['origin']
    proof = request.json['proof']
    distillery = request.json['distillery']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    whiskey = Whiskey_Collection(whiskey, origin, proof, distillery, user_token=user_token)

    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskeys', methods = ['GET'])
@token_required
def get_whiskey(current_user_token):
    a_user = current_user_token.token
    whiskeys = Whiskey_Collection.query.filter_by(user_token = a_user).all()
    response = whiskeys_schema.dump(whiskeys)
    return jsonify(response)


@api.route('/whiskeys/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    whiskey = Whiskey_Collection.query.get(id)
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskeys/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = Whiskey_Collection.query.get(id)
    whiskey.whiskey = request.json['whiskey']
    whiskey.origin = request.json['origin']
    whiskey.proof = request.json['proof']
    whiskey.distillery = request.json['distillery']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskeys/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = Whiskey_Collection.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)