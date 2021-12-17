import datetime
from flask import Flask, jsonify, request, send_file
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required)
from flask_cors import CORS

from handler.ticket_handler import capacity_increase_by_student, lessons_from_another_section
from handler.user_handler import find_user_by_username_and_password

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():
    try:
        params = request.get_json()
        username = str(params['username'])
        password = str(params['password'])
    except Exception as ex:
        print(ex)
        return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

    try:
        response = find_user_by_username_and_password(username, password)
        access_token = create_access_token(identity=username)
        if response.get('Status') == 'OK':
            response['token'] = access_token
            # print(response)
            return jsonify(response), 200
        else:
            # print(response)
            return jsonify(response), 403
    except Exception as ex:
        # print(ex)
        return jsonify(status='ERROR', message='مشکلی رخ داده هست'), 400


@app.route('/create-ticket', methods=['POST'])
@jwt_required()
def create_ticket():
    try:
        user_id = get_jwt_identity()
        params = request.get_json()
        subject = str(params['subject'])
    except Exception as ex:
        print(ex)
        return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

    if subject == 'capacity_increase':
        try:
            receiver_id = params['receiver_id']
            description = params['description']
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = capacity_increase_by_student(user_id, receiver_id, description, course_id)
        if response.get('Status') == 'OK':
            return jsonify(response), 200
        else:
            return jsonify(response), 403

    elif subject == 'lessons_from_another_section':
        try:
            receiver_id = params['receiver_id']
            description = params['description']
            course_id = params['course_id']
            url = params['url']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = lessons_from_another_section(user_id, receiver_id, description, course_id,url)
        if response.get('Status') == 'OK':
            return jsonify(response), 200
        else:
            return jsonify(response), 403

    elif subject == 'class_change_time':
        try:
            receiver_id = params['receiver_id']
            description = params['description']
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400


if __name__ == '__main__':
    app.run()
