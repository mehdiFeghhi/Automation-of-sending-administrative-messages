import datetime

import jdatetime
from sqlalchemy.sql.elements import and_

from handler.connect_db import session
from handler.model.modelDB import EducationAssistant, Course, PermittedCourse, Professor, Student, \
    InitialCourseSelection, Semester, Period_Course_Selection, PresentedCourse, ProfessorLinkPresentedCourse


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


def is_in_period_of_student_course_selection(course_section):
    find_query = Period_Course_Selection.query.filter(
        and_(Period_Course_Selection.role == 'student',
             Period_Course_Selection.course_section == course_section)).first()
    today = datetime.date.today()
    if find_query is None:
        return False
    elif find_query.start_date > today or find_query.end_date < today:
        return False
    else:
        return True


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


# TODO course is he get before or not have prerequested it not be show add orientation
def permitted_course_student(user_id):
    student = Student.query.filter(Student.student_number == user_id).first()
    is_time_of_course_selection = is_in_period_of_student_course_selection(student.cross_section)
    if not is_time_of_course_selection:
        return {'Status': 'ERROR', 'message': 'در بازه انتخاب واحد نیستیم.'}

    permitted_course_list = PermittedCourse.query.filter(PermittedCourse.cross_section == student.cross_section).all()
    print(student.cross_section)
    year, semester = give_year_mount()
    initial_course_list = InitialCourseSelection.query.filter(InitialCourseSelection.student_number == user_id,
                                                              InitialCourseSelection.semester == semester,
                                                              InitialCourseSelection.year == year).all()
    list_not_show_permitted_course = []
    for obj in initial_course_list:
        list_not_show_permitted_course.append(obj.permittedCourse_id)
    list_send = []
    for obj in permitted_course_list:
        if obj.permittedCourse_id not in list_not_show_permitted_course:
            print(obj.professor_id)
            if obj.professor is not None:
                name_professor = obj.professor.user.firs_name + " " + obj.professor.user.last_name
            else:
                name_professor = ""
            course_section = obj.cross_section
            orientation = obj.course.orientation.name
            unit_numbers = obj.course.numbers_unit
            course_name = obj.course.name
            id_permitted_Course = obj.permittedCourse_id
            list_send.append({'name_professor': name_professor, 'course_section': course_section,
                              'orientation': orientation, 'unit_numbers': unit_numbers,
                              'id_permitted_course': id_permitted_Course, 'course_name': course_name})

    return {'Status': 'OK', 'data': list_send}


def permitted_course_eduassignment_prof():
    permitted_course_list = PermittedCourse.query.all()
    year, semester = give_year_mount()
    list_send = []

    for obj in permitted_course_list:
        # print(obj.professor_id)
        # print(obj.professor)
        if obj.professor is not None:
            name_professor = obj.professor.user.firs_name + " " + obj.professor.user.last_name
        else:
            name_professor = ""
        course_section = obj.cross_section
        orientation = obj.course.orientation.name
        unit_numbers = obj.course.numbers_unit
        course_name = obj.course.name
        id_permitted_Course = obj.permittedCourse_id
        number_get_it_in_initial_course_this_term = InitialCourseSelection.query.filter(
            InitialCourseSelection.permittedCourse_id == obj.permittedCourse_id,
            InitialCourseSelection.year == year,
            InitialCourseSelection.semester == semester).count()
        list_send.append(
            {'name_professor': name_professor, 'course_section': course_section, 'orientation': orientation,
             'unit_numbers': unit_numbers, 'id_permitted_course': id_permitted_Course,
             'number_get_it_in_initial_course_this_term': number_get_it_in_initial_course_this_term,
             'course_name': course_name})

    return {'Status': 'OK', 'data': list_send}


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
        return {'Status': 'ERROR', 'message': 'شخص موردنظر دسترسی ندارد نیست'}


def is_this_course_exist(course_id):
    course = session.query(Course).filter(Course.id == course_id).first()
    if course is None:
        return False
    return True


def create_permitted_courses(user_id, course_id_list, course_section):
    is_user_assignment_eduction = is_assignment_education(user_id)

    if not is_user_assignment_eduction:
        return {'Status': 'ERROR', 'message': 'شخص موردنظر مسئول آموزش نیست'}

    elif course_section not in ['bachelor', 'master']:
        return {'Status': 'ERROR', 'message': 'مقطع مربوطه وجود ندارد'}

    list_permitted_course_add = []
    for course_id in course_id_list:
        is_course_exist = is_this_course_exist(course_id)
        is_this_permitted_course_exist = PermittedCourse.query.filter(PermittedCourse.course_id == course_id,
                                                                      PermittedCourse.cross_section == course_section).first()
        # res = create_permitted_course(user_id, course_id, course_section)

        if not is_course_exist:
            return {'Status': 'ERROR', 'message': 'یک درس موردنظر موجود نیست'}
        elif is_this_permitted_course_exist is not None:
            return {'Status': 'ERROR', 'message': 'این درس قبلا وجود داشته است'}
        else:
            list_permitted_course_add.append(PermittedCourse(course_id=course_id, cross_section=course_section,
                                                             educationAssistant_id=user_id))
    session.add_all(list_permitted_course_add)
    session.commit()
    return {'Status': 'OK', 'message': 'دروس با موفقیت در سیستم ثبت شد'}


def create_permitted_course(user_id, course_id, course_section):
    is_user_assignment_eduction = is_assignment_education(user_id)
    is_course_exist = is_this_course_exist(course_id)
    is_this_permitted_course_exist = PermittedCourse.query.filter(PermittedCourse.course_id == course_id,
                                                                  PermittedCourse.cross_section == course_section).first()

    if not is_user_assignment_eduction:
        return {'Status': 'ERROR', 'message': 'شخص موردنظر مسئول آموزش نیست'}

    elif not is_course_exist:
        return {'Status': 'ERROR', 'message': 'درس موردنظر موجود نیست'}

    elif course_section not in ['bachelor', 'master']:
        return {'Status': 'ERROR', 'message': 'مقطع مربوطه وجود ندارد'}
    elif is_this_permitted_course_exist is not None:
        return {'Status': 'ERROR', 'message': 'این درس قبلا وجود داشته است'}
    else:

        new_permitted_course = PermittedCourse(course_id=course_id, cross_section=course_section,
                                               educationAssistant_id=user_id)
        session.add(new_permitted_course)
        session.commit()
        return {'Status': 'OK', 'message': 'این درس با موفقیت در سیستم ثبت شد'}


def is_this_permitted_course_ok_for_this_student(student: Student, list_id_permitted_course) -> bool:
    year, semester = give_year_mount()
    for id_permitted_Course in list_id_permitted_course:

        permitted_course = PermittedCourse.query.filter(
            PermittedCourse.permittedCourse_id == id_permitted_Course).first()
        if permitted_course is None:
            print({'Status': 'ERROR', 'message': 'این انتخاب واحد وجود ندارد.'})
            return False
        initial_course = InitialCourseSelection.query.filter(
            InitialCourseSelection.permittedCourse_id == id_permitted_Course,
            InitialCourseSelection.student_number == student.student_number,
            InitialCourseSelection.semester == semester,
            InitialCourseSelection.year == year).first()
        if initial_course is not None:
            print({'Status': 'ERROR', 'message': 'این درس قبلا توسط شخص انتخاب شده است.'})
            return False

        if permitted_course.cross_section != student.cross_section:
            print({'Status': 'ERROR', 'message': 'مقاطع یکسان نیست. '})
            return False

    return True


def add_initial_course(user_id, list_id_permitted_course):
    student = Student.query.filter(Student.student_number == user_id).first()
    is_time_of_course_selection = is_in_period_of_student_course_selection(student.cross_section)

    if not is_time_of_course_selection:
        return {'Status': 'ERROR', 'message': 'در بازه انتخاب واحد نیستیم.'}

    is_this_person_student = is_person_student(user_id)
    student = Student.query.filter(Student.student_number == user_id).first()
    this_permitted_course_ok = is_this_permitted_course_ok_for_this_student(student, list_id_permitted_course)
    year, semester = give_year_mount()
    if not is_this_person_student:
        return {'Status': 'ERROR', 'message': 'این شخص دانشجو نیست .'}
    if not this_permitted_course_ok:
        return {'Status': 'ERROR', 'message': 'این انتخاب واحد برای این شخص مجاز نیست .'}
    else:

        list_of_initial_course = []
        for id_permitted_Course in list_id_permitted_course:
            list_of_initial_course.append(InitialCourseSelection(student_number=user_id, year=year, semester=semester,
                                                                 permittedCourse_id=id_permitted_Course))
        session.add_all(list_of_initial_course)
        session.commit()
        return {'Status': 'OK', 'message': 'انتخاب واحد مقدماتی شما با موفقیت ثبت شد.'}


def find_initial_course_selection(user_id):
    year, semester = give_year_mount()
    is_this_person_student = is_person_student(user_id)
    if not is_this_person_student:
        return {'Status': 'ERROR', 'message': 'این شخص دانشجو نیست .'}

    initial_course_list = InitialCourseSelection.query.filter(and_(InitialCourseSelection.student_number == user_id,
                                                                   InitialCourseSelection.year == year,
                                                                   InitialCourseSelection.semester == semester)).all()
    list_dic = []
    for initial_course_selection in initial_course_list:
        list_dic.append({'id_initial_course_selection': initial_course_selection.id,
                         'course_name': initial_course_selection.PermittedCourse.course.name,
                         'orientation': initial_course_selection.PermittedCourse.course.orientation.name,
                         'unit_numbers': initial_course_selection.PermittedCourse.course.numbers_unit
                         })

    return {'Status': 'OK', 'data': list_dic}


def delete_permitted_course_by(permitted_course_id, user_id):
    is_user_assignment_eduction = is_assignment_education(user_id)
    if not is_user_assignment_eduction:
        return {'Status': 'ERROR', 'message': 'شخص موردنظر مسئول آموزش نیست'}

    PermittedCourse.query.filter(PermittedCourse.permittedCourse_id == permitted_course_id).delete()
    session.commit()
    return {'Status': 'OK', 'message': 'با موفقیت تغییر اعمال شد.'}


# TODO : ADD some presented course by this function that should be add in another where
def update_permitted_course_prof_by(permitted_course_id, professor_id, user_id):
    is_user_assignment_eduction = is_assignment_education(user_id)

    if not is_user_assignment_eduction:
        return {'Status': 'ERROR', 'message': 'شخص موردنظر مسئول آموزش نیست'}

    permitted_course = PermittedCourse.query.filter(PermittedCourse.permittedCourse_id == permitted_course_id).first()
    if permitted_course is None:
        return {'Status': 'ERROR', 'message': 'همچین درسی موجود نیست .'}

    course_id = permitted_course.course_id
    year, semester = give_year_mount()

    find_present_course = PresentedCourse.query.filter(
        and_(PresentedCourse.course_id == course_id, PresentedCourse.year == year,
             PresentedCourse.semester == semester)).first()

    if find_present_course is None:
        presented_course = PresentedCourse(course_id=course_id, year=year, semester=semester)
        session.add(presented_course)
        # professorLinkPresentedCourse_three = ProfessorLinkPresentedCourse(professor_email=,
        #                                                                   presentedCourse=15)
        session.commit()

    else:
        presented_course = find_present_course

    find_present_course = PresentedCourse.query.filter(
        and_(PresentedCourse.course_id == course_id, PresentedCourse.year == year,
             PresentedCourse.semester == semester)).first()
    if find_present_course is None:
        return {'Status': 'ERROR', 'message': 'خطایی  در سیسم رخ داده هست .'}

    professorLinkPresentedCourse = ProfessorLinkPresentedCourse.query.filter(
        and_(ProfessorLinkPresentedCourse.professor_email == professor_id,
             ProfessorLinkPresentedCourse.presentedCourse == presented_course.id)).first()

    if professorLinkPresentedCourse is None:
        professorLinkPresentedCourse = ProfessorLinkPresentedCourse(professor_email=professor_id,
                                                                     presentedCourse=find_present_course.course_id)
    else:

        professorLinkPresentedCourse.professor_email = professor_id
    session.add(professorLinkPresentedCourse)
    permitted_course.professor_id = professor_id
    session.commit()
    return {'Status': 'OK', 'message': 'با موفقیت تغییر اعمال شد.'}


def delete_initial_course_by(id_initial_course_selection, user_id):
    is_this_person_student = is_person_student(user_id)
    if not is_this_person_student:
        return {'Status': 'ERROR', 'message': 'این شخص دانشجو نیست .'}

    initial_course_selection = InitialCourseSelection.query.filter(
        InitialCourseSelection.id == id_initial_course_selection).first()

    if initial_course_selection is None:
        return {'Status': 'ERROR', 'message': 'این انتخاب واحد وجود ندارد.'}

    elif initial_course_selection.student_number != user_id:
        return {'Status': 'ERROR', 'message': 'این شخص همچین درسی را انتخاب واحد ننموده.'}

    else:

        InitialCourseSelection.query.filter(InitialCourseSelection.id == id_initial_course_selection).delete()
        session.commit()

        return {'Status': 'OK', 'message': 'با موفقیت تغییر اعمال شد.'}


def create_course_selection_period(course_section, term, start_date, end_date, role, user_id):
    is_user_assignment_eduction = is_assignment_education(user_id)
    if not is_user_assignment_eduction:
        return {'Status': 'ERROR', 'message': 'شخص موردنظر مسئول آموزش نیست'}
    elif course_section not in ['bachelor', 'master']:
        return {'Status': 'ERROR', 'message': 'مقطع مربوطه وجود ندارد'}
    elif term not in [1, 2, 3]:
        return {'Status': 'ERROR', 'message': 'داده مربوط به ترم اشتباه هست.'}

    elif role not in ['student', 'professor']:
        return {'Status': 'ERROR', 'message': 'داده مربوط به نقش اشتباه هست.'}
    # print(role)
    elif start_date > end_date:
        return {'Status': 'ERROR', 'message': 'زمان شروع بعد از زمان پایان هست .'}

    find_query = Period_Course_Selection.query.filter(and_(Period_Course_Selection.role == role
                                                           ,
                                                           Period_Course_Selection.course_section == course_section)).first()
    if find_query is None:
        x = Period_Course_Selection(course_section=course_section, role=role, semester=Semester(term),
                                    start_date=start_date, end_date=end_date)
        session.add(x)

    else:
        find_query.role = role
        find_query.course_section = course_section
        find_query.semester = Semester(term)
        find_query.start_date = start_date
        find_query.end_date = end_date

    session.commit()
    return {'Status': 'OK', 'message': 'با موفقیت بازه ثبت نام مقدماتی اعمال شد.'}


def make_gero_to_jalali(time_gero):
    time = jdatetime.GregorianToJalali(time_gero.year, time_gero.month, time_gero.day)
    return "/".join([str(time.jyear), str(time.jmonth), str(time.jday)])


def is_time_of_course_section(user_id):
    is_user_assignment_eduction = is_assignment_education(user_id)
    is_this_person_professor = is_person_professor(user_id)
    is_period_of_student_bachelor = is_in_period_of_student_course_selection('bachelor')
    is_period_of_student_master = is_in_period_of_student_course_selection('master')
    is_this_person_student = is_person_student(user_id)
    if is_user_assignment_eduction or is_this_person_professor:
        if is_period_of_student_master and is_period_of_student_bachelor:
            find_query_bachelor = Period_Course_Selection.query.filter(and_(Period_Course_Selection.role == 'student',
                                                                            Period_Course_Selection.course_section == 'bachelor')).first()
            find_query_master = Period_Course_Selection.query.filter(and_(Period_Course_Selection.role == 'student',
                                                                          Period_Course_Selection.course_section == 'master')).first()
            return {'Status': 'OK', 'Flag': True, 'course_section': 'master_bachelor',
                    'data': [{'role': find_query_bachelor.role,
                              'course_section': find_query_bachelor.course_section,
                              'start_date': make_gero_to_jalali(find_query_bachelor.start_date),
                              'end_date': make_gero_to_jalali(find_query_bachelor.end_date)},
                             {'role': find_query_master.role,
                              'course_section': find_query_master.course_section,
                              'start_date': make_gero_to_jalali(find_query_master.start_date),
                              'end_date': make_gero_to_jalali(find_query_master.end_date)
                              }]}

        elif is_period_of_student_bachelor:
            find_query = Period_Course_Selection.query.filter(and_(Period_Course_Selection.role == 'student',
                                                                   Period_Course_Selection.course_section == 'bachelor')).first()
            return {'Status': 'OK', 'Flag': True, 'course_section': find_query.course_section,
                    'data': [{'role': find_query.role,
                              'course_section': find_query.course_section,
                              'start_date': make_gero_to_jalali(find_query.start_date),
                              'end_date': make_gero_to_jalali(find_query.end_date)}]}
        elif is_period_of_student_master:
            find_query = Period_Course_Selection.query.filter(and_(Period_Course_Selection.role == 'student',
                                                                   Period_Course_Selection.course_section == 'master')).first()
            return {'Status': 'OK', 'Flag': True, 'course_section': find_query.course_section,
                    'data': [{'role': find_query.role,
                              'course_section': find_query.course_section,
                              'start_date': make_gero_to_jalali(find_query.start_date),
                              'end_date': make_gero_to_jalali(find_query.end_date)}]}
        else:
            return {'Status': 'OK', 'Flag': False}
    elif is_this_person_student:
        student = Student.query.filter(Student.student_number == user_id).first()

        is_period_of_this_student = is_in_period_of_student_course_selection(student.cross_section)
        if is_period_of_this_student:
            find_query = Period_Course_Selection.query.filter(and_(Period_Course_Selection.role == 'student',
                                                                   Period_Course_Selection.course_section == student.cross_section)).first()
            return {'Status': 'OK', 'Flag': True, 'course_section': find_query.course_section,
                    'data': {'role': find_query.role,
                             'course_section': find_query.course_section,
                             'start_date': make_gero_to_jalali(find_query.start_date),
                             'end_date': make_gero_to_jalali(find_query.end_date)}}
        else:
            return {'Status': 'OK', 'Flag': False}

    else:
        return {'Status': 'ERROR', "message": "شخص موردنظر معتبر نیست."}
