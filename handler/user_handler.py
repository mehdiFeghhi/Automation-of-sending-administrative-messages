import hashlib

from sqlalchemy.orm import sessionmaker
from handler.connect_db import session
from sqlalchemy import and_, create_engine
from handler.model.modelDB import User, Student, Professor, Advisor, EducationAssistant, Supervisor, DepartmentHead, \
    ResponsibleTraining


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
