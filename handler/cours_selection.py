import jdatetime

from handler.connect_db import session
from handler.model.modelDB import EducationAssistant, Course, PermittedCourse, Professor, Student, \
    InitialCourseSelection, Semester


def give_year_mount():
    year = str(jdatetime.date.today().year)
    month = jdatetime.date.today().month

    if 6 <= month < 11:
        semester = Semester(1)
    elif 11 <= month < 2:
        semester = Semester(2)
    else:
        semester = Semester(3)

    return year, semester


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


def permitted_course_student(user_id):
    student = Student.query.filter(student_number=user_id).first()
    permitted_course_list = PermittedCourse.query.filter(cross_section=student.cross_section).all()
    year, semester = give_year_mount()
    initial_course_list = InitialCourseSelection.query.filter(student_number=user_id, semester=semester,
                                                              year=year).all()
    list_not_show_permitted_course = []
    for obj in initial_course_list:
        list_not_show_permitted_course.append(obj.permittedCourse_id)
    list_send = []
    for obj in permitted_course_list:
        if obj.id not in list_not_show_permitted_course:
            name_professor = obj.professor.user.firs_name + " " + obj.professor.user.last_name
            course_section = obj.course_section
            orientation = obj.course.orientation.name
            unit_numbers = obj.course.unitnumber
            id_permitted_Course = obj.id
            list_send.append({'name_professor': name_professor, 'course_section': course_section,
                              'orientation': orientation, 'unit_numbers': unit_numbers,
                              'id_permitted_Course': id_permitted_Course})

    return {'status': 'OK', 'data': list_send}


def permitted_course_eduassignment_prof():
    permitted_course_list = PermittedCourse.query.all()
    year, semester = give_year_mount()
    list_send = []

    for obj in permitted_course_list:
        name_professor = obj.professor.user.firs_name + " " + obj.professor.user.last_name
        course_section = obj.course_section
        orientation = obj.course.orientation.name
        unit_numbers = obj.course.unitnumber
        id_permitted_Course = obj.id
        number_get_it_in_initial_course_this_term = InitialCourseSelection.query.filter(permittedCourse_id=obj.id,
                                                                                        year=year,
                                                                                        semester=semester).count()
        list_send.append(
            {'name_professor': name_professor, 'course_section': course_section, 'orientation': orientation,
             'unit_numbers': unit_numbers, 'id_permitted_Course': id_permitted_Course,
             'number_get_it_in_initial_course_this_term': number_get_it_in_initial_course_this_term})

    return {'status': 'OK', 'data': list_send}


def find_permitted_courses(user_id):
    is_this_person_student = is_person_student(user_id)
    is_this_person_professor = is_person_professor(user_id)
    is_user_assignment_eduction = is_assignment_education(user_id)
    if is_this_person_student:
        resp = permitted_course_student(user_id)
        return resp
    elif is_this_person_professor or is_user_assignment_eduction:
        resp = permitted_course_eduassignment_prof()
        return resp
    else:
        return {'status': 'ERROR', 'message': 'شخص موردنظر دسترسی ندارد نیست'}


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
