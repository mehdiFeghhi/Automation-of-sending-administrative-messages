from sqlalchemy import Column, Integer, String, DATETIME, Time, Float
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import enum

engine = create_engine('sqlite:///sample.db', echo=True)
Base = declarative_base()


class EnumCourseStatus(enum.Enum):
    finish = "Finish"
    remove = "remove"
    in_process = "in_process"


class Semester(enum.Enum):
    First = 1
    Second = 2
    Summer = 3


class StatusStep(enum.Enum):
    Unread = 1
    Read = 2
    Answered = 3


class Chart(Base):
    __tablename__ = 'charts'
    id = Column(Integer, primary_key=True)

    courses = relationship('Course', secondary='chartLinkCourse')


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    numbers_unit = Column(Integer, nullable=False)

    charts = relationship(Chart, secondary='chartLinkCourse')

    prerequisites_courses = relationship('Course', secondary='preCourseLinkCourse')
    needed_courses = relationship('Course', secondary='needCourseLinkCourse')


class PresentedCourse(Base):
    __tablename__ = 'presentedCourse'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    courses = relationship(Course, backref=backref('presentedCourse', cascade="all,delete"))

    class_name = Column(String)
    time_final_exam = Column(String)

    professors = relationship('Professor', secondary='professorLinkPresentedCourse')


class TimePresentedCourse(Base):
    __tablename__ = 'timePresentedCourse'

    presented_course_id = Column(Integer, ForeignKey('timePresentedCourse.id'))
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


class Student(Base):
    __tablename__ = 'students'

    student_number = Column(String, ForeignKey('users.username'), primary_key=True)
    user = relationship('User', backref=backref('students', uselist=False, cascade="all,delete"))
    time_enter = Column(String, nullable=False)
    chart_id = Column(Integer, ForeignKey('charts.id'))
    chart = relationship("Chart", backref("students"))


# User.educationAssistants = relationship("EducationAssistant", order_by=EducationAssistant.id, back_populates='User')

class Professor(Base):
    __tablename__ = 'professors'

    email = Column(String, ForeignKey('users.username'), primary_key=True)
    user = relationship('User', backref=backref('professors', uselist=False, cascade="all,delete"))


class ProfessorLinkPresentedCourse(Base):
    __tablename__ = 'professorLinkPresentedCourse'

    professor_email = relationship(
        String,
        ForeignKey('professors.email'),
        primary_key=True
    )
    presentedCourse = relationship(
        Integer,
        ForeignKey('presentedCourse.id'),
        primary_key=True
    )


class Advisor(Base):
    __tablename__ = 'advisor'
    id = Column(Integer, primary_key=True)

    email = Column(String, ForeignKey('professors.email'), nullable=False)
    professor = relationship('Professor', backref=backref('advisor'))
    time_enter_student = Column(String, nullable=False)


class DepartmentHead(Base):
    __tablename__ = 'departmentHeads'

    id = Column(Integer, primary_key=True)
    email = Column(String, ForeignKey('professors.email'), nullable=False)
    professor = relationship('Professor', backref=backref('departmentHeads'))

    date_start_duty = Column(DATETIME, nullable=False)
    date_end_duty = Column(DATETIME)


class StudentCourseDate(Base):
    __tablename__ = 'studentCourseDates'

    presentedCourse_id = Column(Integer, ForeignKey('presentedCourse.id'), primary_key=True)
    presentedCourse = relationship(PresentedCourse, backref=backref('studentCourseDates'))

    student_number = Column(String, ForeignKey('students.student_number'), primary_key=True)
    student = relationship(Student, backref=backref('studentCourseDates'))

    mark = Column(Float)
    status = Column(EnumCourseStatus)


class PermittedCourse(Base):
    __tablename__ = 'permittedCourses'

    year = Column(Integer, primary_key=True)
    semester = Column(Semester, primary_key=True)

    course_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course = relationship(Course, backref=backref('permittedCourses'))

    educationAssistant_id = Column(String, ForeignKey('educationAssistants.id'))
    educationAssistants = relationship(EducationAssistant, backref=backref('permittedCourses'))

    initialCourseSelections = relationship('InitialCourseSelection', back_populates='permittedCourses')


class InitialCourseSelection(Base):
    __tablename__ = 'initialCourseSelection'

    student_number = Column(String, ForeignKey('students.student_number'), primary_key=True)
    student = relationship(Student, backref=backref('initialCourseSelection'))

    permittedCourse_year = Column(Integer, ForeignKey('permittedCourses.year'), primary_key=True)
    permittedCourse_semester = Column(Integer, ForeignKey('permittedCourses.semester'), primary_key=True)
    permittedCourse_id = Column(Integer, ForeignKey('permittedCourses.course_id'), primary_key=True)

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


class Step(Base):
    __tablename__ = 'step'

    id = Column(Integer, primary_key=True)

    ticket_id = Column(Integer, ForeignKey('ticket.id'))
    ticket = relationship(Ticket, backref=backref('step'))

    attach_file = Column(String)
    message = Column(String)
    status_step = Column(StatusStep)

    step_before_id = Column(Integer, ForeignKey('step.id'))
    step = relationship('Step', backref=backref('step'))
