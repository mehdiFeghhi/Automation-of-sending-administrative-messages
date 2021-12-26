from sqlalchemy import and_, or_
from sqlalchemy import asc, desc
from handler.model.modelDB import Student, Course, Professor, PresentedCourse, Semester, PreCourseLinkCourse, \
    ProfessorLinkPresentedCourse, Supervisor, Ticket, Step, EducationAssistant, User, StatusStep, DepartmentHead, \
    Advisor, StudentCourseData, ChartLinkCourse
from handler.connect_db import session
import jdatetime


# TODO : check step if not end return True else return false
def check_step_this_ticket_is_finish_or_not(tickets):
    return False


# TODO : check this course just in sinore chart
def is_this_course_in_sinore_chart(course_id):

    query = session.query(ChartLinkCourse).filter(
        and_(ChartLinkCourse.course_id == course_id, ChartLinkCourse.chart_id == 2)).first()

    if query is None:
        return False
    return True


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
    year, semester = give_year_mount()
    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    # professor = session.query(Professor).filter(Professor.email == receiver_id).first()

    if student is None:
        return {'Status': "ERROR", 'error': "this user isn't student."}
    elif course is None:
        return {'Status': "ERROR", 'error': "this course wasn't found."}
    # elif professor is None:
    #     return {'Status': "ERROR", 'error': "this professor isn't exist."}
    presentedCourse = session.query(PresentedCourse).filter(and_(PresentedCourse.course_id == course_id,
                                                                 PresentedCourse.year == year,
                                                                 PresentedCourse.semester == semester)).first()
    if presentedCourse is None:
        return {'Status': "ERROR", 'error': "this course haven't any present Course in this semester."}

    professorLinkPresentedCourse1 = session.query(ProfessorLinkPresentedCourse).filter(
        ProfessorLinkPresentedCourse.presentedCourse == presentedCourse.id).first()
    if professorLinkPresentedCourse1 is None:
        return {'Status': "ERROR", 'error': "this professor haven't this course."}
    professor_email = professorLinkPresentedCourse1.professor_email

    flag = is_this_ticket_is_exist_or_finish(topic='capacity_increase', course_relation=course_id, year=year,
                                             semester=semester)
    if not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='capacity_increase', message=description, course_relation=course_id)
    step = Step(receiver_id=professor_email)
    step.ticket = ticket
    session.add(step)
    session.commit()
    return {'Status': "OK"}


def lessons_from_another_section(user_id, receiver_id, description, url):
    print("in lessons_from_another_section")
    print(user_id)
    print(receiver_id)
    print(description)

    year, semester = give_year_mount()

    student = session.query(Student).filter(Student.student_number == user_id).first()
    #
    # educationAssistant = session.query(EducationAssistant).filter(and_(EducationAssistant.username == receiver_id,
    #                                                                    EducationAssistant.date_end_duty.is_(
    #                                                                        None))).first()
    educationAssistant = session.query(EducationAssistant).filter(EducationAssistant.date_end_duty.is_(None)).first()

    flag = is_this_ticket_is_exist_or_finish_two('lessons_from_another_section', year, semester)

    if student is None:
        return {'Status': "ERROR", 'error': "this user isn't student."}

    elif educationAssistant is None:
        return {'Status': "ERROR", 'error': "this person isn't education assistant."}

    elif not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='lessons_from_another_section', message=description, attach_file=url)
    step = Step(receiver_id=educationAssistant.username)
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

    year, semester = give_year_mount()

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    # educationAssistant = session.query(EducationAssistant).filter(and_(EducationAssistant.username == receiver_id,
    #                                                                    EducationAssistant.date_end_duty.is_(
    #                                                                        None))).first()
    educationAssistant = session.query(EducationAssistant).filter(EducationAssistant.date_end_duty.is_(
        None)).first()

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
    step = Step(receiver_id=educationAssistant.username)
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
    year, semester = give_year_mount()

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    educationAssistant = session.query(EducationAssistant).filter(EducationAssistant.date_end_duty.is_(None)).first()

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
    step = Step(receiver_id=educationAssistant.username)
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

    year, semester = give_year_mount()

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    educationAssistant = session.query(EducationAssistant).filter(EducationAssistant.date_end_duty.is_(
        None)).first()
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
    step = Step(receiver_id=educationAssistant.username)
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
    year, semester = give_year_mount()

    student = session.query(Student).filter(Student.student_number == user_id).first()
    course = session.query(Course).filter(Course.id == course_id).first()

    # educationAssistant = session.query(EducationAssistant).filter(and_(EducationAssistant.username == receiver_id,
    #                                                                    EducationAssistant.date_end_duty.is_(
    #                                                                        None))).first()
    educationAssistant = session.query(EducationAssistant).filter(EducationAssistant.date_end_duty.is_(
        None)).first()

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

    flag = is_this_ticket_is_exist_or_finish(topic='course_from_another_orientation', course_relation=course_id,
                                             year=year,
                                             semester=semester)
    if not flag:
        return {'Status': "ERROR", 'error': "you give this request before please be calm."}

    ticket = Ticket(sender=user_id, topic='course_from_another_orientation', message=description,
                    course_relation=course_id)
    step = Step(receiver_id=educationAssistant.username)
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

    sender_is_user = True if session.query(User).filter(User.username == user_id).first() is not None else False
    receiver_is_user = True if session.query(User).filter(User.username == receiver_id).first() is not None else False
    course = session.query(Course).filter(Course.id == course_id).first()

    if sender_is_user is False:
        return {'Status': "ERROR", 'error': "this user sender isn't exist."}
    elif course is None:
        return {'Status': "ERROR", 'error': "this course wasn't found."}
    elif receiver_is_user is False:
        return {'Status': "ERROR", 'error': "this user receiver isn't exist."}

    ticket = Ticket(sender=user_id, topic=subject, message=description, course_relation=course_id, attach_file=url)
    step = Step(receiver_id=receiver_id)
    step.ticket = ticket
    session.add(step)
    session.commit()

    return {'Status': "OK"}


def delete_ticket_user(user_id, ticket_id, ):
    ticket = session.query(Ticket).filter(and_(Ticket.id == ticket_id, Ticket.sender == user_id)).first()
    if ticket is None:
        return {'Status': "ERROR", 'error': "this ticket not belong to this person."}
    else:
        session.query(Step).filter(Step.ticket_id == ticket_id).update(
            {Step.status_step: StatusStep(6)})
        session.commit()
        return {'Status': "OK"}


def department_accept(step_one):
    next_receiver_Department_head = session.query(DepartmentHead).filter(
        DepartmentHead.date_end_duty.is_(None)).first()
    next_step = Step(receiver_id=next_receiver_Department_head.email,
                     parent_id=step_one.id,
                     ticket_id=step_one.ticket_id)

    session.add(next_step)
    session.commit()


def education_assistant_accept(step_one):
    next_receiver_educationAssistant = session.query(EducationAssistant).filter(
        EducationAssistant.date_end_duty.is_(None)).first()
    next_step = Step(receiver_id=next_receiver_educationAssistant.username,
                     parent_id=step_one.id,
                     ticket_id=step_one.ticket_id)

    session.add(next_step)
    session.commit()


def professor_accept(step_one, ticket):
    year, semester = give_year_mount()

    presentedCourse = session.query(PresentedCourse).filter(
        and_(PresentedCourse.course_id == ticket.course_relation, PresentedCourse.semester == semester,
             PresentedCourse.year == year)
    ).first()
    professorLinkPresentedCourse = session.query(ProfessorLinkPresentedCourse).fitler(ProfessorLinkPresentedCourse.presentedCourse == presentedCourse).first()

    email_proffessor = professorLinkPresentedCourse.professor_email

    next_step = Step(receiver_id='Tohidi@gmail.com',
                     parent_id=step_one.id,
                     ticket_id=step_one.ticket_id)

    session.add(next_step)
    session.commit()


def advisor_accept(step_one, ticket):
    student_user = session.query(Student).filter(
        Student.student_number == ticket.user.username
    ).first()
    next_receiver_advisor = student_user.adviser
    next_step = Step(receiver_id=next_receiver_advisor.email,
                     parent_id=step_one.id,
                     ticket_id=step_one.ticket_id)

    session.add(next_step)
    session.commit()


def supervisor_accept(step_one, ticket):
    student_user = session.query(Student).filter(
        Student.student_number == ticket.user.username
    ).first()
    next_receiver_supervisor = student_user.supervisor
    next_step = Step(receiver_id=next_receiver_supervisor.email,
                     parent_id=step_one.id,
                     ticket_id=step_one.ticket_id)

    session.add(next_step)
    session.commit()


def update_ticket_user(user_id, ticket_id, step, massage, url):
    steps_of_user = session.query(Step).filter(and_(Step.ticket_id == ticket_id, Step.receiver_id == user_id,
                                                    or_(Step.status_step == StatusStep(1),
                                                        Step.status_step == StatusStep(2)))).all()

    ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
    if len(steps_of_user) != 1:
        return {'Status': "ERROR", 'error': "there is a problem about step."}
    step_one = steps_of_user[0]
    step_one.status_step = step
    if massage is not None:
        step_one.message = massage
    if url is not None:
        step_one.attach_file = url
    session.commit()
    if step == StatusStep(3):
        step_number = session.query(Step).filter(Step.ticket_id == ticket_id).count()
        if ticket.topic == 'capacity_increase':
            if step_number == 1:
                department_accept(step_one)
            elif step_number == 2:
                education_assistant_accept(step_one)
            elif step_number == 3:
                step_one.status_step = StatusStep(7)
                session.commit()
        elif ticket.topic == 'lessons_from_another_section':

            if step_number == 1:
                user_to_give_professor_accept_id = ticket.sender
                next_step = Step(receiver_id=user_to_give_professor_accept_id,
                                 parent_id=step_one.id)

                session.add(next_step)
                session.commit()
            elif step_number == 2:
                department_accept(step_one)
            elif step_number == 3:
                education_assistant_accept(step_one)
            elif step_number == 4:
                step_one.status_step = StatusStep(7)
                session.commit()

        elif ticket.topic == 'class_change_time' or ticket.topic == 'exam_time_change':
            if step_number == 1:
                professor_accept(step_one, ticket)
            elif step_number == 2:
                department_accept(step_one)

            elif step_number == 3:
                education_assistant_accept(step_one)
            elif step_number == 4:
                step_one.status_step = StatusStep(7)
                session.commit()

        elif ticket.topic == 'master_course_request':

            if step_number == 1:
                advisor_accept(step_one, ticket)
            elif step_number == 2:
                professor_accept(step_one, ticket)

            elif step_number == 3:
                department_accept(step_one)

            elif step_number == 4:
                education_assistant_accept(step_one)

            elif step_number == 5:
                step_one.status_step = StatusStep(7)
                session.commit()
        elif ticket.topic == 'course_from_another_orientation':
            if step_number == 1:
                supervisor_accept(step_one, ticket)
            elif step_number == 2:
                professor_accept(step_one, ticket)
            elif step_number == 3:
                department_accept(step_one)

            elif step_number == 4:
                education_assistant_accept(step_one)

            elif step_number == 5:
                step_one.status_step = StatusStep(7)
                session.commit()

    return {'Status': "OK"}


def get_procedure_steps(procedure):
    if (procedure == 'lessons_from_another_section'):
        return {
            0: "دانشجو",
            1: "مسئول آموزش",
            2: "معاونت آموزشی",
            3: "رئیس بخش",
            4: "مسئول آموزش"
        }
    elif (procedure == 'capacity_increase'):
        return {
            0: "دانشجو",
            1: "مسئول آموزش",
            2: "استاد درس",
            3: "رئیس بخش",
            4: "مسئول آموزش"
        }
    elif (procedure == 'class_change_time'):
        return {
            0: "دانشجو",
            1: "مسئول آموزش",
            2: "استاد درس",
            3: "مسئول آموزش"
        }
    elif (procedure == 'exam_time_change'):
        return {
            0: "دانشجو",
            1: "مسئول آموزش",
            2: "استاد درس",
            3: "مسئول آموزش"
        }
    elif (procedure == 'master_course_request'):
        return {
            0: "دانشجو",
            1: "مسئول آموزش",
            2: "استاد مشاور",
            3: "استاد درس",
            4: "رئیس بخش",
            4: "مسئول آموزش"
        }
    elif (procedure == 'course_from_another_orientation'):
        return {
            0: "دانشجو",
            1: "مسئول آموزش",
            2: "استاد راهنما",
            3: "استاد درس",
            4: "رئیس بخش",
            5: "مسئول آموزش"
        }


def get_tickets_handler(user_id):
    response = []
    sent_tickets = session.query(Ticket).filter(Ticket.sender == user_id).all()
    received_tickets = session.query(Step).filter(Step.receiver_id == user_id).all()
    for ticket in sent_tickets:
        all_steps = get_procedure_steps(ticket.topic)
        steps = session.query(Step).filter(Step.ticket_id == ticket.id).order_by(asc(Step.id)).all()
        sender = session.query(User).filter(User.username == ticket.sender).first()
        step_num = 0
        for step in steps:
            step_num += 1
            descriptions = {step_num: step.message,
                            # "status": step.status_step
                            }
        response.append({"id": ticket.id,
                         "sender_id": sender.username,
                         "sender_fname": sender.firs_name,
                         "sender_lname": sender.last_name,
                         "message": ticket.message,
                         "type_ticket": ticket.topic,
                         "created_date": ticket.exact_time_create,
                         "descriptions": descriptions,
                         "current_step": {step_num: steps[-1].message},
                         "all_steps": all_steps})

    for step in received_tickets:
        ticket_id = step.ticket_id
        parent_ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        sender = session.query(User).filter(User.username == parent_ticket.sender).first()

        all_steps = get_procedure_steps(parent_ticket.topic)

        rest_steps = session.query(Step).filter(Step.ticket_id == ticket_id).order_by(asc(Step.id)).all()
        step_num = 0
        for step in rest_steps:
            step_num += 1
            descriptions = {step_num: step.message,
                            # "status": step.status_step
                            }

        response.append({"id": ticket_id,
                         "sender_id": sender.username,
                         "sender_fname": sender.firs_name,
                         "sender_lname": sender.last_name,
                         "message": parent_ticket.message,
                         "type_ticket": parent_ticket.topic,
                         "created_date": parent_ticket.exact_time_create,
                         "descriptions": descriptions,
                         "current_step": {step_num: rest_steps[-1].message},
                         "all_steps": all_steps})
    return response


def get_receivers_handler(user_id):
    curr_dep_head = session.query(DepartmentHead).order_by(desc(DepartmentHead.date_start_duty)).first()
    res = []
    if (user_id == curr_dep_head.email):
        prof_list = session.query(Professor).all()
        for prof in prof_list:
            user = session.query(User).filter(User.username == prof.email).first()
            prof_data = {
                "id": user.username,
                "fname": user.firs_name,
                "lname": user.last_name
            }
            res.append(prof_data)
        ed_assistant = session.query(EducationAssistant).first()
        user = session.query(User).filter(User.username == ed_assistant.username).first()
        supervisor_info = {
            "id": user.username,
            "fname": user.firs_name,
            "lname": user.last_name
        }
        res.append(supervisor_info)
        return res

    # elif(session.query(Advisor).filter(Advisor.id == user_id).first() != None):

    # elif(session.query(Supervisor).filter(Supervisor.id == user_id).first() != None):

    else:
        student = session.query(Student).filter(Student.student_number == user_id).first()
        dep_head_user = session.query(User).filter(User.username == curr_dep_head.email).first()
        dep_head_data = {
            "id": dep_head_user.username,
            "fname": dep_head_user.firs_name,
            "lname": dep_head_user.last_name
        }
        res.append(dep_head_data)
        prof_list = session.query(Professor).all()
        for prof in prof_list:
            user = session.query(User).filter(User.username == prof.email).first()
            prof_data = {
                "id": user.username,
                "fname": user.firs_name,
                "lname": user.last_name
            }
            res.append(prof_data)

        advisor = session.query(User).filter(User.username == student.adviser_id).first()
        advisor_data = {
            "id": user.username,
            "fname": user.firs_name,
            "lname": user.last_name
        }
        res.append(advisor_data)
        ed_assistant = session.query(EducationAssistant).first()
        user = session.query(User).filter(User.username == ed_assistant.username).first()
        supervisor_info = {
            "id": user.username,
            "fname": user.firs_name,
            "lname": user.last_name
        }
        res.append(supervisor_info)

        return res
