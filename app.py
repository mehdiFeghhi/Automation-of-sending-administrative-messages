import datetime
from flask import Flask, jsonify, request, send_file
from flask_jwt_extended import (
    JWTManager, create_access_token, get_jwt_identity, jwt_required)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
from sqlalchemy.sql.functions import user

from handler.cours_selection import find_permitted_courses, create_permitted_course
from handler.model.modelDB import StatusStep, Supervisor
from handler.ticket_handler import capacity_incresessase_by_student, lessons_from_another_section, class_change_time, \
    master_course_request, course_from_another_orientation, exam_time_change, normal_ticket, delete_ticket_user, \
    update_ticket_user, get_tickets_handler, get_receivers_handler, get_inprograss_tickets_handler
from handler.user_handler import find_user_by_username_and_password, find_user_by_user_id, get_professors_handler, \
    create_students_handler
from handler.course_handler import get_course_list, get_orientations_handler, create_course_handler

from config import create_app

app = create_app()


@app.cli.command('initDB')
def init_db():
    from init_db import init_db
    init_db()


@app.route('/api/login', methods=['POST'])
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
            return jsonify(response), 401
    except Exception as ex:
        # print(ex)
        return jsonify(status='ERROR', message='مشکلی رخ داده هست'), 400


@app.route('/api/is-authentication', methods=['GET'])
@jwt_required()
def is_authentication_this_user():
    try:
        user_id = get_jwt_identity()
        response = find_user_by_user_id(user_id)
        return jsonify(response), 200
    except Exception as ex:
        return jsonify(status='ERROR', message='همچین توکنی وجود ندارد'), 400


@app.route('/api/create-ticket', methods=['POST'])
@jwt_required()
def create_ticket():
    try:
        user_id = get_jwt_identity()
        print(user_id)
        params = request.get_json()
        receiver_id = params.get('receiver_id')
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

        response = capacity_incresessase_by_student(
            user_id, receiver_id, description, course_id)

    elif subject == 'lessons_from_another_section':
        # try:
        #     course_id = params['course_id']
        #     url = params.get('url')
        # except Exception as ex:
        #     print(ex)
        #     return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400
        url = params.get('url')
        response = lessons_from_another_section(
            user_id, receiver_id, description, url)
    elif subject == 'class_change_time':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = class_change_time(
            user_id, receiver_id, description, course_id)

    elif subject == 'exam_time_change':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = exam_time_change(
            user_id, receiver_id, description, course_id)

    elif subject == 'master_course_request':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = master_course_request(
            user_id, receiver_id, description, course_id)

    elif subject == 'course_from_another_orientation':
        try:
            course_id = params['course_id']
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400

        response = course_from_another_orientation(
            user_id, receiver_id, description, course_id)

    else:

        course_id = params.get('course_id')
        url = params.get('url')
        response = normal_ticket(user_id, receiver_id,
                                 subject, description, course_id, url)

    if response.get('Status') == 'OK':
        return jsonify(response), 201
    else:
        return jsonify(response), 400


@app.route('/api/step-ticket', methods=['POST', 'PUT'])
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

    if request.method == 'POST':
        response = delete_ticket_user(user_id, id_ticket)
        if response.get('Status') == 'OK':
            return jsonify(response), 200
        else:
            return jsonify(response), 204

    else:
        try:
            step_fr = params['step']
            step_number = ['read', 'accept', 'reject'].index(step_fr) + 2
            step = StatusStep(step_number)
            massage = params['massage']
            url = params.get('url')
        except Exception as ex:
            print(ex)
            return jsonify(status='ERROR', message='داده ارسالی اشتباه است 2'), 400
        response = update_ticket_user(user_id, id_ticket, step, massage, url)
        if response.get('Status') == 'OK':
            return jsonify(response), 200
        else:
            return jsonify(response), 400


@app.route('/api/get-courses', methods=['GET'])
def get_courses():
    try:
        # print(get_cosurse_list())
        return jsonify(get_course_list()), 200

    except Exception as ex:
        print(ex)
        return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400


@app.route('/api/get-tickets', methods=['GET'])
@jwt_required()
def get_tickets():
    user_id = get_jwt_identity()
    return jsonify(get_tickets_handler(user_id))


@app.route('/api/get-tickets-inprogress', methods=['GET'])
@jwt_required()
def get_inprograss_tickets():
    user_id = get_jwt_identity()
    return jsonify(get_inprograss_tickets_handler(user_id))


@app.route('/api/get-receivers', methods=['GET'])
@jwt_required()
def get_receivers():
    user_id = get_jwt_identity()
    return jsonify(get_receivers_handler(user_id))

@app.route('/api/get-orientations', methods=['GET'])
def get_orientation():
    return jsonify(get_orientations_handler())

@app.route('/api/add-course', methods=['post'])
@jwt_required()
def create_course():
    user_id = get_jwt_identity()
    params = request.get_json()
    response = create_course_handler(user_id,
                                     params["name_course"],
                                     params["orientation"],
                                     params["unit_numbers"],
                                     params["prerequisites"])
    if response.get('Status') == 'OK':
        return jsonify(response), 201
    else:
        return jsonify(response), 401

@app.route('/api/get-professors', methods=['GET'])
def get_professors():
    return jsonify(get_professors_handler()), 200

@app.route('/api/add-student', methods=['post'])
@jwt_required()
def create_student():
    user_id = get_jwt_identity()
    params = request.get_json()
    resp = create_students_handler(user_id,
                            params['student_number'],
                            params['first_name'],
                            params['last_name'],
                            params['password'],
                            params['orientation'],
                            params['cross_section'],
                            params['enter_year'],
                            params['adviser_id'],
                            params['superviser_id'])
    if(resp['Status'] == 'شما مجوز انجام اینکار را ندارید'):
        return resp, 401
    
    if(resp['Status'] == 'شماره دانشجویی تکراری است'):
        return resp, 400
    
    if(resp['Status'] == 'استاد مشاور وجود ندارد'):
        return resp, 400

    return resp, 201



@app.route('/api/add-permitted-course', methods=['POST'])
@jwt_required()
def add_permitted_course():
    try:
        user_id = get_jwt_identity()
        params = request.get_json()
        course_section = params['course_section']
        course_id = params['course_id']
        response = create_permitted_course(user_id, course_id, course_section)
        if response.get('Status') == 'OK':
            return jsonify(response), 201
        else:
            return jsonify(response), 401

    except Exception as ex:
        print(ex)
        return jsonify(status='ERROR', message='داده ارسالی اشتباه است'), 400


@app.route('/api/get-permitted-course', methods=['GET'])
@jwt_required()
def get_permitted_courses():
    user_id = get_jwt_identity()

    response = find_permitted_courses(user_id)

if __name__ == '__main__':
    app.run()
