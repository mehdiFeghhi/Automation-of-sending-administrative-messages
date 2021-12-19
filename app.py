import datetime
from flask import Flask, jsonify, request, send_file
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required)
from flask_cors import CORS

from handler.model.modelDB import StatusStep
from handler.ticket_handler import capacity_incresessase_by_student, lessons_from_another_section, class_change_time, \
    master_course_request, course_from_another_orientation, exam_time_change, normal_ticket, delete_ticket_user, \
    update_ticket_user
from handler.user_handler import find_user_by_username_and_password
from handler.course_handler import get_course_list

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
            return jsonify(response), 204
    except Exception as ex:
        # print(ex)
        return jsonify(status='ERROR', message='مشکلی رخ داده هست'), 400


@app.route('/create-ticket', methods=['POST'])
@jwt_required()
def create_ticket():
    try:
        user_id = get_jwt_identity()
        print(user_id)
        params = request.get_json()
        receiver_id = params['receiver_id']
        description = params['description']
        subject = str(params['subject'])
    except Exception as ex:
        print(ex)
        return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

    if subject == 'capacity_increase':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = capacity_incresessase_by_student(user_id, receiver_id, description, course_id)

    elif subject == 'lessons_fromnother_section':
        # try:
        #     course_id = params['course_id']
        #     url = params.get('url')
        # except Exception as ex:
        #     print(ex)
        #     return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400
        url = params.get('url')
        response = lessons_from_another_section(user_id, receiver_id, description, url)
    elif subject == 'class_change_time':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = class_change_time(user_id, receiver_id, description, course_id)

    elif subject == 'exam_time_change':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = exam_time_change(user_id, receiver_id, description, course_id)

    elif subject == 'master_course_request':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = master_course_request(user_id, receiver_id, description, course_id)

    elif subject == 'course_from_another_orientation':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = course_from_another_orientation(user_id, receiver_id, description, course_id)

    else:

        course_id = params.get('course_id')
        url = params.get('url')
        response = normal_ticket(user_id, receiver_id, subject, description, course_id, url)

    if response.get('Status') == 'OK':
        return jsonify(response), 201
    else:
        return jsonify(response), 204


@app.route('/step-ticket', methods=['DELETE', 'PUT'])
@jwt_required()
def work_with_step_ticket():
    try:
        user_id = get_jwt_identity()
        print(user_id)
        params = request.get_json()
        id_ticket = params['id_ticket']
    except Exception as ex:
        print(ex)
        return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

    if request.method == 'DELETE':
        response = delete_ticket_user(user_id, id_ticket)
        if response.get('Status') == 'OK':
            return jsonify(response), 200
        else:
            return jsonify(response), 204

    else:
        try:
            step_fr = params['step']
            step_number = ['read', 'accept', 'reject'].index(step_fr) + 1
            step = StatusStep(step_number)
            massage = params['massage']
            url = params.get('url')
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400
        response = update_ticket_user(user_id, id_ticket, step, massage, url)
        if response.get('Status') == 'OK':
            return jsonify(response), 200
        else:
            return jsonify(response), 204

@app.route('/get-courses', methods=['GET'])
def get_courses():
    try:
        # print(get_cosurse_list())
        return jsonify(get_course_list()), 200
        
    except Exception as ex:
        print(ex)
        return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

    


if __name__ == '__main__':
    app.run()