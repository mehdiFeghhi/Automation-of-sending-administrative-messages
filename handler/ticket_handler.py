from sqlalchemy import and_

from handler.model.modelDB import Student, Course, Professor, PresentedCourse, Semester, PreCourseLinkCourse, \
    ProfessorLinkPresentedCourse, Ticket, Step, EducationAssistant, User
from handler.connect_db import session
import jdatetime


# TODO : check step if not end return True else return false
def check_step_this_ticket_is_finish_or_not(tickets):
    return False
# TODO : check this course just in sinore chart
def is_this_course_in_sinore_chart(course_id):
    return True

def is_this_ticket_is_exist_or_finish(topic, course_relation, year, semester):
    tickets = session.query(Ticket).filter(and_(Ticket.topic == topic, Ticket.course_relation == course_relation,
                                                Ticket.year_create == year, Ticket.semester == semester)).all()
    if len(tickets) > 0:
        return check_step_this_ticket_is_finish_or_not(tickets)
    else:
        return True


def is_this_ticket_is_exist_or_finish_two(topic, year, semester):
    tickets = session.query(Ticket).filter(and_(Ticket.topic == topic,
                                                Ticket.year_create == year, Ticket.semester == semester)).all()
    if len(tickets) > 0:
        return check_step_this_ticket_is_finish_or_not(tickets)
    else:
        return True


def capacity_incresessase_by_student(user_id, receiver_id, description, course_id):
    print("in capacity_increase_by_student")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    year = str(jdatetime.date.today().year)
    month = jdatetime.date.today().month

    if 6 <= month < 10:
        semester = Semester(1)
    elif 10 <= month < 2:
        semester = Semester(2)
    else:
        semester = Semester(3)

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    professor = session.query(Professor).filter(Professor.email == receiver_id).first()

    if student is None:
        return {'Status': "ERROR", 'error': "this user isn't student."}
    elif course is None:
        return {'Status': "ERROR", 'error': "this course wasn't found."}
    elif professor is None:
        return {'Status': "ERROR", 'error': "this professor isn't exist."}
    presentedCourse = session.query(PresentedCourse).filter(and_(PresentedCourse.course_id == course_id,
                                                                 PresentedCourse.year == year,
                                                                 PresentedCourse.semester == semester)).first()
    if presentedCourse is None:
        return {'Status': "ERROR", 'error': "this course haven't any present Course in this semester."}

    preCourseLinkCourse = session.query(ProfessorLinkPresentedCourse).filter(
        and_(ProfessorLinkPresentedCourse.professor_email == professor.email,
             ProfessorLinkPresentedCourse.presentedCourse == presentedCourse.id)).first()

    if preCourseLinkCourse is None:
        return {'Status': "ERROR", 'error': "this professor haven't this course."}

    flag = is_this_ticket_is_exist_or_finish(topic='capacity_increase', course_relation=course_id, year=year,
                                             semester=semester)
    if not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='capacity_increase', message=description, course_relation=course_id)
    step = Step(receiver_id=receiver_id)
    step.ticket = ticket
    session.add(step)
    session.commit()
    return {'Status': "OK"}


def lessons_from_another_section(user_id, receiver_id, description, url):
    print("in lessons_from_another_section")
    print(user_id)
    print(receiver_id)
    print(description)

    year = str(jdatetime.date.today().year)
    month = jdatetime.date.today().month

    if 6 <= month < 10:
        semester = Semester(1)
    elif 10 <= month < 2:
        semester = Semester(2)
    else:
        semester = Semester(3)

    student = session.query(Student).filter(Student.student_number == user_id).first()

    educationAssistant = session.query(EducationAssistant).filter(and_(EducationAssistant.username == receiver_id,
                                                                       EducationAssistant.date_end_duty.is_(
                                                                           None))).first()
    flag = is_this_ticket_is_exist_or_finish_two('lessons_fromnother_section', year, semester)

    if student is None:
        return {'Status': "ERROR", 'error': "this user isn't student."}

    elif educationAssistant is None:
        return {'Status': "ERROR", 'error': "this person isn't education assistant."}

    elif not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='lessons_fromnother_section', message=description, attach_file=url)
    step = Step(receiver_id=receiver_id)
    step.ticket = ticket
    session.add(step)
    session.commit()

    return {'Status': "OK"}


def class_change_time(user_id, receiver_id, description, course_id):
    print("in class_change_time")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    year = str(jdatetime.date.today().year)
    month = jdatetime.date.today().month

    if 6 <= month < 10:
        semester = Semester(1)
    elif 10 <= month < 2:
        semester = Semester(2)
    else:
        semester = Semester(3)

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    educationAssistant = session.query(EducationAssistant).filter(and_(EducationAssistant.username == receiver_id,
                                                                       EducationAssistant.date_end_duty.is_(
                                                                           None))).first()
    if student is None:
        return {'Status': "ERROR", 'error': "this user isn't student."}
    elif course is None:
        return {'Status': "ERROR", 'error': "this course wasn't found."}
    elif educationAssistant is None:
        return {'Status': "ERROR", 'error': "this educationAssistant isn't exist."}
    presentedCourse = session.query(PresentedCourse).filter(and_(PresentedCourse.course_id == course_id,
                                                                 PresentedCourse.year == year,
                                                                 PresentedCourse.semester == semester)).first()
    if presentedCourse is None:
        return {'Status': "ERROR", 'error': "this course haven't any present Course in this semester."}

    flag = is_this_ticket_is_exist_or_finish(topic='class_change_time', course_relation=course_id, year=year,
                                             semester=semester)
    if not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='class_change_time', message=description, course_relation=course_id)
    step = Step(receiver_id=receiver_id)
    step.ticket = ticket
    session.add(step)
    session.commit()
    return {'Status': "OK"}


def exam_time_change(user_id, receiver_id, description, course_id):
    print("in exam_time_change")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    year = str(jdatetime.date.today().year)
    month = jdatetime.date.today().month

    if 6 <= month < 10:
        semester = Semester(1)
    elif 10 <= month < 2:
        semester = Semester(2)
    else:
        semester = Semester(3)

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    educationAssistant = session.query(EducationAssistant).filter(and_(EducationAssistant.username == receiver_id,
                                                                       EducationAssistant.date_end_duty.is_(
                                                                           None))).first()
    if student is None:
        return {'Status': "ERROR", 'error': "this user isn't student."}
    elif course is None:
        return {'Status': "ERROR", 'error': "this course wasn't found."}
    elif educationAssistant is None:
        return {'Status': "ERROR", 'error': "this educationAssistant isn't exist."}
    presentedCourse = session.query(PresentedCourse).filter(and_(PresentedCourse.course_id == course_id,
                                                                 PresentedCourse.year == year,
                                                                 PresentedCourse.semester == semester)).first()
    if presentedCourse is None:
        return {'Status': "ERROR", 'error': "this course haven't any present Course in this semester."}

    flag = is_this_ticket_is_exist_or_finish(topic='exam_time_change', course_relation=course_id, year=year,
                                             semester=semester)
    if not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='exam_time_change', message=description, course_relation=course_id)
    step = Step(receiver_id=receiver_id)
    step.ticket = ticket
    session.add(step)
    session.commit()
    return {'Status': "OK"}




def master_course_request(user_id, receiver_id, description, course_id):
    print("in master_course_request")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)

    year = str(jdatetime.date.today().year)
    month = jdatetime.date.today().month

    if 6 <= month < 10:
        semester = Semester(1)
    elif 10 <= month < 2:
        semester = Semester(2)
    else:
        semester = Semester(3)

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    educationAssistant = session.query(EducationAssistant).filter(and_(EducationAssistant.username == receiver_id,
                                                                       EducationAssistant.date_end_duty.is_(
                                                                           None))).first()
    if student is None:
        return {'Status': "ERROR", 'error': "this user isn't student."}
    elif student.cross_section != 'masters':
        return {'Status': "ERROR", 'error': "this user isn't masters student."}

    elif course is None:
        return {'Status': "ERROR", 'error': "this course wasn't found."}
    elif not is_this_course_in_sinore_chart(course.id):
        return {'Status': "ERROR", 'error': "this course wasn't senior course."}
    elif educationAssistant is None:
        return {'Status': "ERROR", 'error': "this educationAssistant isn't exist."}
    presentedCourse = session.query(PresentedCourse).filter(and_(PresentedCourse.course_id == course_id,
                                                                 PresentedCourse.year == year,
                                                                 PresentedCourse.semester == semester)).first()
    if presentedCourse is None:
        return {'Status': "ERROR", 'error': "this course haven't any present Course in this semester."}

    flag = is_this_ticket_is_exist_or_finish(topic='master_course_request', course_relation=course_id, year=year,
                                             semester=semester)
    if not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='master_course_request', message=description, course_relation=course_id)
    step = Step(receiver_id=receiver_id)
    step.ticket = ticket
    session.add(step)
    session.commit()

    return {'Status': "OK"}


def course_from_another_orientation(user_id, receiver_id, description, course_id):
    print("in course_from_another_orientation")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)

    year = str(jdatetime.date.today().year)
    month = jdatetime.date.today().month

    if 6 <= month < 10:
        semester = Semester(1)
    elif 10 <= month < 2:
        semester = Semester(2)
    else:
        semester = Semester(3)

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    educationAssistant = session.query(EducationAssistant).filter(and_(EducationAssistant.username == receiver_id,
                                                                       EducationAssistant.date_end_duty.is_(
                                                                           None))).first()
    if student is None:
        return {'Status': "ERROR", 'error': "this user isn't student."}
    elif student.cross_section != 'senior':
        return {'Status': "ERROR", 'error': "this user isn't senior student."}

    elif course is None:
        return {'Status': "ERROR", 'error': "this course wasn't found."}

    elif course.orientation == student.orientation:
        return {'Status': "ERROR", 'error': "this course is in your orientation."}
    elif educationAssistant is None:
        return {'Status': "ERROR", 'error': "this educationAssistant isn't exist."}
    presentedCourse = session.query(PresentedCourse).filter(and_(PresentedCourse.course_id == course_id,
                                                                 PresentedCourse.year == year,
                                                                 PresentedCourse.semester == semester)).first()
    if presentedCourse is None:
        return {'Status': "ERROR", 'error': "this course haven't any present Course in this semester."}

    flag = is_this_ticket_is_exist_or_finish(topic='course_from_another_orientation', course_relation=course_id, year=year,
                                             semester=semester)
    if not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='course_from_another_orientation', message=description, course_relation=course_id)
    step = Step(receiver_id=receiver_id)
    step.ticket = ticket
    session.add(step)
    session.commit()
    return {'Status': "OK"}


def normal_ticket(user_id, receiver_id, subject, description, course_id, url):
    print("in normal_ticket")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)

    sender_is_user = True if session.query(User).filter(User.username == user_id).first() is None else False
    receiver_is_user = True if session.query(User).filter(User.username == receiver_id).first() is None else False
    course = session.query(Course).filter(Course.id == course_id).first()

    if sender_is_user is False:
        return {'Status': "ERROR", 'error': "this user isn't exist."}
    elif course is None:
        return {'Status': "ERROR", 'error': "this course wasn't found."}
    elif receiver_is_user is False:
        return {'Status': "ERROR", 'error': "this user isn't exist."}

    ticket = Ticket(sender=user_id, topic=subject, message=description, course_relation=course_id, attach_file=url)
    step = Step(receiver_id=receiver_id)
    step.ticket = ticket
    session.add(step)
    session.commit()

    return {'Status': "OK"}
