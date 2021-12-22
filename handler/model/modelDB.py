from sqlalchemy import Column, Integer, String, DATETIME, Time, Float, Enum
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import jdatetime

import enum

engine = create_engine('sqlite:///sample.db', echo=True)
Base = declarative_base()


class EnumCourseStatus(enum.IntEnum):
    finish = 0
    remove = 1
    in_process = 2


class Semester(enum.IntEnum):
    First = 1
    Second = 2
    Summer = 3


class StatusStep(enum.IntEnum):
    Unread = 1
    Read = 2
    Accept = 3
    Reject = 4
    Answered = 5
    Finish = 6
    Ended_step = 7


class Chart(Base):
    __tablename__ = 'charts'
    id = Column(Integer, primary_key=True)
    educationAssistants_create_id = Column(Integer, ForeignKey('educationAssistants.id'))
    educationAssistants_create = relationship('EducationAssistant', backref=backref('charts'))

    name = Column(String(50), nullable=False)
    year_create = Column(String(20), nullable=False)

    courses = relationship('Course', secondary='chartLinkCourse')


class Orientation(Base):
    __tablename__ = 'orientations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # courses = relationship('Course', backref=backref('orientations'))


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    numbers_unit = Column(Integer, nullable=False)

    charts = relationship(Chart, secondary='chartLinkCourse')

    # prerequisites_courses = relationship
    # prerequisites_courses_parent = relationship('Course', secondary='preCourseLinkCourse')

    # needed_courses_first = relationship('Course', secondary='needCourseLinkCourse')
    # needed_courses_second = relationship('Course', secondary='needCourseLinkCourse')

    orientation_id = Column(Integer, ForeignKey('orientations.id'))
    orientation = relationship(Orientation, backref=backref('courses'))


class PresentedCourse(Base):
    __tablename__ = 'presentedCourse'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    courses = relationship(Course, backref=backref('presentedCourse', cascade="all,delete"))

    year = Column(String, nullable=False)
    semester = Column(Enum(Semester), nullable=False)

    class_name = Column(String)
    time_final_exam = Column(String)

    professors = relationship('Professor', secondary='professorLinkPresentedCourse')


class TimePresentedCourse(Base):
    __tablename__ = 'timePresentedCourse'

    id = Column(Integer, primary_key=True)
    presented_course_id = Column(Integer, ForeignKey('presentedCourse.id'))
    presented_course = relationship(PresentedCourse, backref=backref('timePresentedCourse', cascade="all,delete"))

    string_name_day = Column(String, nullable=False)
    times_start = Column(Time)


class PreCourseLinkCourse(Base):
    __tablename__ = 'preCourseLinkCourse'

    course_parent = Column(
        Integer,
        ForeignKey('courses.id'),
        primary_key=True
    )
    course_child = Column(
        Integer,
        ForeignKey('courses.id'),
        primary_key=True
    )
    course = relationship(Course, foreign_keys='PreCourseLinkCourse.course_parent')
    preCourse = relationship(Course, foreign_keys='PreCourseLinkCourse.course_child')


class NeedCourseLinkCourse(Base):
    __tablename__ = 'needCourseLinkCourse'

    first_course = Column(
        Integer,
        ForeignKey('courses.id'),
        primary_key=True
    )
    second_course = Column(
        Integer,
        ForeignKey('courses.id'),
        primary_key=True
    )
    course = relationship(Course, foreign_keys='NeedCourseLinkCourse.first_course')
    needCourse = relationship(Course, foreign_keys='NeedCourseLinkCourse.second_course')


class ChartLinkCourse(Base):
    __tablename__ = 'chartLinkCourse'

    chart_id = Column(
        Integer,
        ForeignKey('charts.id'),
        primary_key=True
    )

    course_id = Column(
        Integer,
        ForeignKey('courses.id'),
        primary_key=True
    )


class User(Base):
    __tablename__ = 'users'
    # id = Column(Integer, primary_key=True)

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    firs_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    picture_file_address = Column(String)

    birthday = Column(DATETIME)
    email_show_all = Column(String)

    # student = relationship('Student', backref=backref('users', uselist=False))
    # professor = relationship('Professor', backref=backref('users', uselist=False))

    # responsibleTrainings = relationship('ResponsibleTraining', backref=backref('users'))
    # educationAssistants = relationship('EducationAssistant', backref=backref('users'))

    # email = Column(String)

    # educationAssistants = relationship(
    #     "EducationAssistant",
    #     order_by=EducationAssistant.id,
    #     back_populates="EducationAssistant",
    #     cascade="all,delete,delete-orphan"
    # )


class EducationAssistant(Base):
    __tablename__ = 'educationAssistants'

    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('users.username'))
    user = relationship("User", backref=backref("educationAssistants", cascade="all,delete"))
    date_start_duty = Column(DATETIME, nullable=False)
    date_end_duty = Column(DATETIME)


class ResponsibleTraining(Base):
    __tablename__ = 'responsibleTrainings'

    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('users.username'))
    user = relationship("User", backref=backref("responsibleTrainings", cascade="all,delete"))
    date_start_duty = Column(DATETIME, nullable=False)
    date_end_duty = Column(DATETIME)


class Student(Base):
    __tablename__ = 'students'

    student_number = Column(String, ForeignKey('users.username'), primary_key=True)
    user = relationship('User', backref=backref('students', uselist=False, cascade="all,delete"))
    time_enter = Column(String, nullable=False)
    chart_id = Column(Integer, ForeignKey('charts.id'))
    chart = relationship("Chart", backref=backref("students"))
    cross_section = Column(String, nullable=False)
    orientation = Column(String, nullable=False)

    adviser_id = Column(Integer, ForeignKey('advisor.id'))
    adviser = relationship('Advisor', backref=backref('students'))

    supervisor_id = Column(Integer, ForeignKey('supervisors.id'))
    supervisor = relationship('Supervisor', backref=backref('students'))


# User.educationAssistants = relationship("EducationAssistant", order_by=EducationAssistant.id, back_populates='User')

class Professor(Base):
    __tablename__ = 'professors'

    email = Column(String, ForeignKey('users.username'), primary_key=True)
    user = relationship('User', backref=backref('professors', uselist=False, cascade="all,delete"))

    # advisors = relationship('Advisor', backref=backref('professors'))
    # departmentHeads = relationship('DepartmentHead', backref=backref('professors'))
    # supervisors = relationship('Supervisor', backref=backref('professors'))

    PresentedCourses = relationship(PresentedCourse, secondary='professorLinkPresentedCourse')


class ProfessorLinkPresentedCourse(Base):
    __tablename__ = 'professorLinkPresentedCourse'

    professor_email = Column(
        String,
        ForeignKey('professors.email'),
        primary_key=True
    )
    presentedCourse = Column(
        Integer,
        ForeignKey('presentedCourse.id'),
        primary_key=True
    )


class Advisor(Base):
    __tablename__ = 'advisor'
    id = Column(Integer, primary_key=True)

    cross_section = Column(String, nullable=False)
    orientation = Column(String, nullable=False)

    email = Column(String, ForeignKey('professors.email'), nullable=False)
    professor = relationship('Professor', backref=backref('advisor'))
    time_enter_student = Column(String, nullable=False)


class Supervisor(Base):
    __tablename__ = 'supervisors'
    id = Column(Integer, primary_key=True)

    cross_section = Column(String, nullable=False)
    orientation = Column(String, nullable=False)

    email = Column(String, ForeignKey('professors.email'), nullable=False)
    professor = relationship('Professor', backref=backref('supervisors'))
    # students = relationship(Student, backref=backref('supervisor'))


class DepartmentHead(Base):
    __tablename__ = 'departmentHeads'

    id = Column(Integer, primary_key=True)
    email = Column(String, ForeignKey('professors.email'), nullable=False)
    professor = relationship('Professor', backref=backref('departmentHeads'))

    date_start_duty = Column(DATETIME, nullable=False)
    date_end_duty = Column(DATETIME)


class StudentCourseData(Base):
    __tablename__ = 'studentCourseDatas'

    presentedCourse_id = Column(Integer, ForeignKey('presentedCourse.id'), primary_key=True)
    presentedCourse = relationship(PresentedCourse, backref=backref('studentCourseDatas'))

    student_number = Column(String, ForeignKey('students.student_number'), primary_key=True)
    student = relationship(Student, backref=backref('studentCourseDatas'))

    mark = Column(Float)
    status = Column(Enum(EnumCourseStatus), default=EnumCourseStatus.in_process)


class PermittedCourse(Base):
    __tablename__ = 'permittedCourses'

    permittedCourse_id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    semester = Column(Enum(Semester), nullable=False)

    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    course = relationship(Course, backref=backref('permittedCourses'))

    educationAssistant_id = Column(String, ForeignKey('educationAssistants.id'))
    educationAssistants = relationship(EducationAssistant, backref=backref('permittedCourses'))

    # initialCourseSelections = relationship('InitialCourseSelection', back_populates='permittedCourses')


class InitialCourseSelection(Base):
    __tablename__ = 'initialCourseSelection'
    id = Column(Integer, primary_key=True)
    student_number = Column(String, ForeignKey('students.student_number'), nullable=False)
    student = relationship(Student, backref=backref('initialCourseSelection'))

    # permittedCourse_year = Column(Integer, ForeignKey('permittedCourses.year'), primary_key=True)
    # permittedCourse_semester = Column(Integer, ForeignKey('permittedCourses.semester'), primary_key=True)
    # permittedCourse_id = Column(Integer, ForeignKey('permittedCourses.course_id'), primary_key=True)

    permittedCourse_id = Column(Integer, ForeignKey('permittedCourses.permittedCourse_id'), nullable=False)
    permittedCourse = relationship(PermittedCourse, backref=backref('initialCourseSelection', cascade="all,delete"))


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    message = Column(String)
    attach_file = Column(String)

    course_relation = Column(Integer, ForeignKey('courses.id'))
    course = relationship(Course, backref=backref('ticket'))

    sender = Column(String, ForeignKey('users.username'))
    user = relationship(User, backref=backref('ticket'))
    exact_time_create = Column(String, default=str(jdatetime.date.today()))
    year_create = Column(String, default=str(jdatetime.date.today().year))
    month = jdatetime.date.today().month
    if 6 <= month < 11:
        semester = Semester(1)
    elif 11 <= month < 2:
        semester = Semester(2)
    else:
        semester = Semester(3)
    semester_create = Column(Enum(Semester), default=semester)


class Step(Base):
    __tablename__ = 'step'

    id = Column(Integer, primary_key=True)

    receiver_id = Column(String, ForeignKey('users.username'), nullable=False)
    user = relationship(User, backref=backref('step'))

    ticket_id = Column(Integer, ForeignKey('ticket.id'))
    ticket = relationship(Ticket, backref=backref('step'))

    attach_file = Column(String)
    message = Column(String)
    status_step = Column(Enum(StatusStep), default=StatusStep(1))

    parent_id = Column(Integer, ForeignKey('step.id'))
    parent_step = relationship('Step', backref=backref('step', remote_side=[id]))


Base.metadata.create_all(engine)
