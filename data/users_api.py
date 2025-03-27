import datetime

import flask
from flask import make_response, jsonify, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'users': [user.to_dict(
        only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'modified_date')) for
        user in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'user': user.to_dict(
        only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'modified_date'))})


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    try:
        surname = request.json['surname']
        name = request.json['name']
        age = request.json['age']
        position = request.json['position']
        speciality = request.json['speciality']
        address = request.json['address']
        email = request.json['email']
        modified_date = datetime.datetime.now()
        # print(request.json)
        if not (isinstance(age, int)):
            raise Exception
    except Exception:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User(
        surname=surname,
        name=name,
        age=age,
        position=position,
        speciality=speciality,
        address=address,
        email=email,
        modified_date=modified_date,
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/edit_users/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found user'}), 404)

    keys_and_type = [('surnamae', str), ('name', str), ('age', int), ('position', str), ('speciality', str),
                     ('address', str), ('email', str)]
    modified_keys_and_values = dict()
    for key, correct_type in keys_and_type:
        value = request.json.get(key, None)
        if value is not None:
            if not isinstance(value, correct_type):
                return make_response(jsonify({'error': 'Bad request'}), 400)
            modified_keys_and_values[key] = value
    if len(modified_keys_and_values) != len(request.json):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    # print(modified_keys_and_values, request.json.keys())
    if 'surname' in modified_keys_and_values:
        user.surname = modified_keys_and_values['surname']
    elif 'name' in modified_keys_and_values:
        user.name = modified_keys_and_values['name']
    elif 'age' in modified_keys_and_values:
        user.age = modified_keys_and_values['age']
    elif 'position' in modified_keys_and_values:
        user.position = modified_keys_and_values['position']
    elif 'speciality' in modified_keys_and_values:
        user.speciality = modified_keys_and_values['speciality']
    elif 'address' in modified_keys_and_values:
        user.address = modified_keys_and_values['address']
    elif 'email' in modified_keys_and_values:
        user.email = modified_keys_and_values['email']
        user.modified_date = datetime.datetime.now()
    db_sess.commit()
    return jsonify({'success': 'OK'})
