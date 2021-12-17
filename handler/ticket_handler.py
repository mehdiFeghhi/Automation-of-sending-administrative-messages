from sqlalchemy import and_

from handler.model.modelDB import Student, Course, Professor, PresentedCourse, Semester, PreCourseLinkCourse, \
    ProfessorLinkPresentedCourse, Ticket, Step
from handler.connect_db import session
import jdatetime


def find_ticket_step(topic, course_relation):
    pass


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

    find_step_of_ticket = find_ticket_step(topic='capacity_increase', course_relation=course_id)

    ticket = Ticket(sender=user_id, topic='capacity_increase', message=description, course_relation=course_id)
    step = Step()
    step.ticket = ticket
    session.add(step)
    session.commit()
    return {'Status': "OK"}


def lessons_from_another_section(user_id, receiver_id, description, course_id, url):
    print("in lessons_from_another_section")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    return {'Status': "OK"}


def class_change_time(user_id, receiver_id, description, course_id):
    print("in class_change_time")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    return {'Status': "OK"}


def exam_time_change(user_id, receiver_id, description, course_id):
    print("in exam_time_change")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    return {'Status': "OK"}


def master_course_request(user_id, receiver_id, description, course_id):
    print("in master_course_request")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    return {'Status': "OK"}


def course_from_another_orientation(user_id, receiver_id, description, course_id):
    print("in mourse_from_another_orientation")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    return {'Status': "OK"}


def normal_ticket(user_id, receiver_id, description, course_id, url):
    print("in normal_ticket")
    print(user_id)
    print(receiver_id)
    print(description)
    print(course_id)
    return {'Status': "OK"}
