import hashlib
from flask_cors.core import probably_regex

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import true
from handler.connect_db import session
from sqlalchemy import and_, create_engine
from handler.model.modelDB import User, Student, Professor, Advisor, EducationAssistant, Supervisor, DepartmentHead, \
    ResponsibleTraining
from datetime import date


def find_main_role_of_person_information(user):
    educationAssistants = session.query(EducationAssistant).filter(EducationAssistant.username == user.username,
                                                                   EducationAssistant.date_end_duty.is_(None)).all()

    professor = session.query(Professor).filter(Professor.email == user.username).all()
    responsibleTrainings = session.query(ResponsibleTraining).filter(and_(ResponsibleTraining.username == user.username,
                                                                          ResponsibleTraining.date_end_duty.is_(
                                                                              None))).all()
    student = session.query(Student).filter(Student.student_number == user.username).all()
    main_role = ""
    if len(educationAssistants) == 1:
        role = educationAssistants[0]
        dic_role = vars(role)
        dic_role.pop('_sa_instance_state')

        dic_role_name = {'name_role': 'educationAssistants'}
        dic_role_name.update(dic_role)
        return dic_role_name, "educationAssistants"

    elif len(professor) == 1:
        role = professor[0]
        dic_role = vars(role)
        dic_role.pop('_sa_instance_state')
        dic_role_name = {'name_role': 'professor'}
        dic_role_name.update(dic_role)

        dic_other_type_of_professor = {}
        departmentHead = session.query(DepartmentHead).filter(and_(DepartmentHead.email == role.email,
                                                                   DepartmentHead.date_end_duty.is_(None))).all()
        if len(departmentHead) == 1:
            dic_departmentHead = vars(departmentHead[0])
            dic_departmentHead.pop('_sa_instance_state')
            main_role = "departmentHead"
            dic_other_type_of_professor['departmentHead'] = dic_departmentHead

        advisers = session.query(Advisor).filter(Advisor.email == role.email).all()
        if len(advisers) > 0:
            advisers_of_year_item = []
            if main_role == "":
                main_role = "advisers"
            for item in advisers:
                advisers_of_year_item.append(
                    {'advisers_id': item.id, 'adviser_time_enter_student': item.time_enter_student})

            dic_other_type_of_professor['advisers'] = advisers_of_year_item
        supervisor = session.query(Supervisor).filter(Supervisor.email == role.email).all()
        if len(supervisor) > 0:
            supervisor_of_year_item = []
            if main_role == "":
                main_role = "supervisors"
            elif main_role == "advisers":
                main_role = "advisers_supervisors"
            for item in supervisor:
                supervisor_of_year_item.append({'supervisor_id': item.id})

            dic_other_type_of_professor['supervisor'] = supervisor_of_year_item

        dic_role_name['type_of_professor'] = dic_other_type_of_professor
        return dic_role_name, main_role


    elif len(responsibleTrainings) == 1:
        role = responsibleTrainings[0]
        dic_role = vars(role)
        dic_role.pop('_sa_instance_state')

        dic_role_name = {'name_role': 'responsibleTrainings'}
        dic_role_name.update(dic_role)
        return dic_role_name, "responsibleTrainings"


    elif len(student) == 1:
        role = student[0]
        dic_role = vars(role)
        dic_role.pop('_sa_instance_state')

        dic_role_name = {'name_role': 'student'}
        dic_role_name.update(dic_role)
        return dic_role_name, "student"

    else:
        raise "user model in db in part role didn't work right "


def find_user_by_username_and_password(user_name: str, password: str):
    hash_password = str(hashlib.sha256(password.encode()).hexdigest())
    result = session.query(User).filter(and_(User.username == user_name, User.password == hash_password)).all()

    if len(result) == 0:
        return {'status': 'ERROR', 'message': 'نام کاربری یا پسورد اشتباه است .'}
    elif len(result) == 1:
        user = result[0]
        role, main_role = find_main_role_of_person_information(user)
        return {'Status': "OK", "user": {'username': user.username, 'first_name': user.firs_name
            , 'last_name': user.last_name, 'picture_file_address': user.picture_file_address,
                                         'birthday': user.birthday, 'email_show_all': user.email_show_all,
                                         "main_role": main_role,
                                         'role': role}}
    else:
        raise "این شخص نمی تواند در دیتابیس به این شکل باشد ."


def find_user_by_user_id(user_id: str):
    result = session.query(User).filter(User.username == user_id).all()
    if len(result) == 0:
        return {'status': 'ERROR'}
    elif len(result) == 1:
        user = result[0]
        role, main_role = find_main_role_of_person_information(user)
        return {'Status': "OK", "user": {'username': user.username, 'first_name': user.firs_name
            , 'last_name': user.last_name, 'picture_file_address': user.picture_file_address,
                                         'birthday': user.birthday, 'email_show_all': user.email_show_all,
                                         "main_role": main_role,
                                         'role': role}}
    else:
        raise "User model in db work wrong"


def get_professors_handler():
    dephead_email = None
    try:
        dephead_email = session.query(DepartmentHead).filter(DepartmentHead.date_end_duty == None).first().email
    except Exception as e:
        pass
    profs = session.query(Professor).all()
    res = []
    for prof in profs:
        prof_data = {'id': prof.email,
                     'fname': prof.user.firs_name,
                     'lname': prof.user.last_name,
                     'is_dep_head': prof.email == dephead_email
                     }
        res.append(prof_data)
    return res


# TODO : can write better Mehdi Feghhi Write and change In Hossain AlahAkbari Code
def is_add_this_professor_to_adviser(cross_section, enter_year, adviser_id, orientation):
    if session.query(Professor).filter(Professor.email == adviser_id).first() == None:
        print("hi")
        return False
    else:

        advisor = Advisor(email=adviser_id, time_enter_student=enter_year, cross_section=cross_section,
                          orientation=orientation)
        session.add(advisor)
        session.commit()
        return True


def create_students_handler(user_id,
                            std_num,
                            firs_name,
                            last_name,
                            password,
                            orientation,
                            cross_section,
                            enter_year,
                            adviser_id,
                            superviser_id):
    if (session.query(EducationAssistant).filter(EducationAssistant.username == user_id).first() == None):
        return {'message': 'شما مجوز انجام اینکار را ندارید'}

    if (session.query(Student).filter(Student.student_number == std_num).first() != None):
        return {'message': 'شماره دانشجویی تکراری است'}

    advisor = session.query(Advisor).filter(Advisor.email == adviser_id).first()
    if (session.query(Advisor).filter(Advisor.email == adviser_id).first() == None):
        if not is_add_this_professor_to_adviser(cross_section, enter_year, adviser_id, orientation):
            return {'message': 'استاد مشاور وجود ندارد'}

    new_user = User(username=std_num, password=str(hashlib.sha256(password.encode()).hexdigest()),
                    firs_name=firs_name,
                    last_name=last_name)

    new_student = Student(student_number=new_user.username, time_enter=enter_year, cross_section=cross_section,
                          orientation=orientation)
    supervisor = session.query(Supervisor).filter(Supervisor.email == superviser_id).first()

    new_student.adviser = advisor
    new_student.supervisor = supervisor

    session.add(new_user)
    session.add(new_student)
    session.commit()
    return {'message': 'OK'}


def create_professor_handler(user_id,
                             first_name,
                             last_name,
                             email,
                             password,
                             is_departman_boss):
    if (session.query(EducationAssistant).filter(EducationAssistant.username == user_id).first() == None):
        return {'message': 'شما مجوز انجام اینکار را ندارید'}

    if (session.query(Professor).filter(Professor.email == email).first() != None):
        return {'message': 'ایمل استاد تکراری است'}

    new_user = User(username=email, password=str(hashlib.sha256(password.encode()).hexdigest()),
                    firs_name=first_name,
                    last_name=last_name)

    new_prof = Professor(email=new_user.username)

    if (is_departman_boss):
        dep_head = DepartmentHead(email=new_prof.email,
                                  date_start_duty=date.today())
        curr_dep_head = session.query(DepartmentHead).filter(DepartmentHead.date_end_duty == None).first()
        if (curr_dep_head != None):
            curr_dep_head.date_end_duty = date.today()
        session.add(dep_head)

    session.add_all([new_user, new_prof])
    session.commit()

    return {'message': 'OK'}


def update_professor_handler(user_id,
                             first_name,
                             last_name,
                             email,
                             new_email,
                             password,
                             is_departman_boss
                             ):
    if (session.query(EducationAssistant).filter(EducationAssistant.username == user_id).first() == None):
        return {'message': 'شما مجوز انجام اینکار را ندارید'}

    prof = session.query(Professor).filter(Professor.email == email).first()
    if (prof == None):
        return {'message': 'استاد یافت نشد'}

    user = session.query(User).filter(User.username == email).first()

    if new_email != None and not (len(new_email) == 0):
        prof.email = new_email
        user.username = new_email


    if (first_name != None):
        user.firs_name = first_name

    if (last_name != None):
        user.last_name = last_name

    if (password != None):
        user.password = str(hashlib.sha256(password.encode()).hexdigest())

    if (is_departman_boss != None):
        if (is_departman_boss):
            current_head = DepartmentHead.query.filter(DepartmentHead.date_end_duty == None).one_or_none()
            if not current_head:
                hed = DepartmentHead(email=prof.email, date_start_duty=date.today())
                session.add(hed)
            elif current_head.email != email:
                current_head.date_end_duty = date.today()
                hed = DepartmentHead(email=prof.email, date_start_duty=date.today())
                session.add(hed)

    session.commit()
    return {'message': 'OK'}


def get_students_handler(user_id):
    resp = []
    if (session.query(EducationAssistant).filter(EducationAssistant.username == user_id).first() == None):
        raise 'شما مجوز انجام اینکار را ندارید'

    students = session.query(Student).all()
    for student in students:
        superviser_email = None
        superviser = session.query(Supervisor).filter(Supervisor.id == student.supervisor_id).first()
        if (superviser != None):
            superviser_email = superviser.email

        std_data = {'first_name': student.user.firs_name,
                    'last_name': student.user.last_name,
                    'student_number': student.student_number,
                    'password': student.user.password,
                    'orientation': student.orientation,
                    'cross_section': student.cross_section,
                    'enter_year': student.time_enter,
                    'adviser_id': student.adviser_id,
                    'superviser_id': student.supervisor_id,
                    'superviser_email': superviser_email
                    }

        resp.append(std_data)

    return resp


def update_student_info(user_id,
                        std_num,
                        new_std_num,
                        firs_name,
                        last_name,
                        password,
                        orientation,
                        cross_section,
                        enter_year,
                        adviser_id,
                        superviser_id):
    if (session.query(EducationAssistant).filter(EducationAssistant.username == user_id).first() == None):
        return {'message': 'شما مجوز انجام اینکار را ندارید'}

    student = session.query(Student).filter(Student.student_number == std_num).first()
    if (student == None):
        return {'message': 'دانشجو یافت نشد'}

    if (firs_name != None):
        student.user.firs_name = firs_name

    if (last_name != None):
        student.user.last_name = last_name

    if (password != None):
        student.user.password = str(hashlib.sha256(password.encode()).hexdigest())

    if (orientation != None):
        student.orientation = orientation

    if (cross_section != None):
        student.cross_section = cross_section

    if (enter_year != None):
        student.time_enter = enter_year

    if (adviser_id != None):
        student.adviser_id = adviser_id

    if (superviser_id != None):
        student.supervisor_id = superviser_id

    if (new_std_num != None):
        if (len(new_std_num) == 0):
            return {'message': 'طول شماره دانشجویی نمیتواند صفر باشد'}
        student.student_number = new_std_num
        student.user.username = new_std_num

    session.commit()
    return {'message': 'OK'}


def change_student_pass_handler(user_id,
                                password):
    student = session.query(Student).filter(Student.student_number == user_id).first()
    if (student == None):
        return {'message': 'شما مجوز انجام اینکار را ندارید'}

    student.user.password = str(hashlib.sha256(password.encode()).hexdigest())
    session.commit()
    return {'message': 'OK'}
