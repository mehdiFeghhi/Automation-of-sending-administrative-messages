from handler.connect_db import session
from handler.model.modelDB import EducationAssistant, Course, PermittedCourse, Professor, Student


def is_assignment_education(user_id):
    educationAssistants = session.query(EducationAssistant).filter(EducationAssistant.username == user_id,
                                                                   EducationAssistant.date_end_duty.is_(None)).all()
    if len(educationAssistants) == 1:
        return True
    else:
        return False


def is_person_professor(user_id):
    professor = session.query(Professor).filter(Professor.email == user_id).all()

    if len(professor) == 1:
        return True
    else:
        return False


def is_person_student(user_id):
    student = session.query(Student).filter(Student.student_number == user_id).all()

    if len(student) == 1:
        return True
    else:
        return False


def find_permitted_courses(user_id):
    is_this_person_student = is_person_student(user_id)
    is_this_person_professor = is_person_professor(user_id)
    is_user_assignment_eduction = is_assignment_education(user_id)
    if is_this_person_student:
        return {}
    elif is_this_person_professor or is_user_assignment_eduction:
        return {}
    else :
        return {'status': 'ERROR', 'message': 'شخص موردنظر ولید نیست'}


def is_this_course_exist(course_id):
    course = session.query(Course).filter(Course.id == course_id).first()
    if course is None:
        return False
    return True


def create_permitted_course(user_id, course_id, course_section):
    is_user_assignment_eduction = is_assignment_education(user_id)
    is_course_exist = is_this_course_exist(course_id)

    if not is_user_assignment_eduction:
        return {'status': 'ERROR', 'message': 'شخص موردنظر مسئول آموزش نیست'}

    elif not is_course_exist:
        return {'status': 'ERROR', 'message': 'درس موردنظر موجود نیست'}

    elif course_section not in ['bachelor', 'master']:
        return {'status': 'ERROR', 'message': 'مقطع مربوطه وجود ندارد'}
    else:

        new_permitted_course = PermittedCourse(course_id=course_id, cross_section=course_section,
                                               educationAssistant_id=course_section)
        session.add(new_permitted_course)
        session.commit()
        return {'status': 'OK', 'Message': 'این شخص با موفقیت در سیستم ثبت شد'}
