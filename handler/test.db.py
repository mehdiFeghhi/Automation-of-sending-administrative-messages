import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib
import jdatetime

from model.modelDB import User, Student, Advisor, Professor, Supervisor, DepartmentHead, EducationAssistant, \
    ResponsibleTraining, Chart, Course, Orientation, ChartLinkCourse, PreCourseLinkCourse, NeedCourseLinkCourse, \
    PresentedCourse, Semester, ProfessorLinkPresentedCourse

file_path = os.path.abspath(os.getcwd()) + "/sample.db"
engine = create_engine('sqlite:///' + file_path, echo=True)

Session = sessionmaker(bind=engine)


def add_item_to_db():
    session = Session()
    user_student_one = User(username='9732527', password=str(hashlib.sha256("1234".encode()).hexdigest()),
                            firs_name='mehdi',
                            last_name='Feghhi')
    student_one = Student(student_number=user_student_one.username, time_enter='1397', cross_section='masters',
                          orientation='computer')

    user_student_two = User(username='9632527', password=str(hashlib.sha256("1234".encode()).hexdigest()),
                            firs_name='hassan',
                            last_name='Abbasi')
    student_tow = Student(student_number=user_student_two.username, time_enter='1396', cross_section='masters',
                          orientation='computer')

    user_student_three = User(username='9732557', password=str(hashlib.sha256("1234".encode()).hexdigest()),
                              firs_name='poay',
                              last_name='fekry')
    student_three = Student(student_number=user_student_three.username, time_enter='1397', cross_section='masters',
                            orientation='computer')
    user_student_four = User(username='9832538', password=str(hashlib.sha256("1234".encode()).hexdigest()),
                             firs_name='reza',
                             last_name='farjam')
    student_four = Student(student_number=user_student_four.username, time_enter='1398', cross_section='masters',
                           orientation='computer')

    user_student_five = User(username='9732517', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                             firs_name='mood',
                             last_name='sharizi')
    student_five = Student(student_number=user_student_five.username, time_enter='1397', cross_section='masters',
                           orientation='computer')

    user_student_six = User(username='9731527', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                            firs_name='hossain',
                            last_name='hedayadtzadeh')
    student_six = Student(student_number=user_student_six.username, time_enter='1397', cross_section='senior',
                          orientation='computer')

    user_student_seven = User(username='9822528', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                              firs_name='sara',
                              last_name='mohammady')
    student_seven = Student(student_number=user_student_seven.username, time_enter='1398', cross_section='senior',
                            orientation='computer')

    user_professor_one = User(username='keshtkaran@gmail.com',
                              password=str(hashlib.sha256("4231".encode()).hexdigest()),
                              firs_name='morteza',
                              last_name='keshtkaran')
    professor_one = Professor(email=user_professor_one.username)

    advisor_one_professor_one = Advisor(cross_section='masters', orientation="computer", email=professor_one.email,
                                        time_enter_student="1397")
    student_one.adviser = advisor_one_professor_one

    user_professor_two = User(username='sami@gmail.com', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                              firs_name='ashkan',
                              last_name='sami')
    professor_two = Professor(email=user_professor_two.username)

    supervisor_one_professor_two = Supervisor(cross_section='Senior', orientation="artificialIntelligence",
                                              email=professor_two.email,
                                              )
    departmentHead_one_professor_two = DepartmentHead(email=professor_two.email,
                                                      date_start_duty=datetime(2019, 5, 17))

    user_professor_three = User(username='taheri@gmail.com', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                                firs_name='mohammdad',
                                last_name='taheri')
    professor_three = Professor(email=user_professor_three.username)
    supervisor_one_professor_three = Supervisor(cross_section='Senior', orientation="artificialIntelligence",
                                                email=professor_three.email,
                                                )

    student_six.supervisor = supervisor_one_professor_three
    student_six.adviser = advisor_one_professor_one

    advisor_one_professor_three = Advisor(cross_section='masters', orientation="computer", email=professor_three.email,
                                          time_enter_student='1396')

    advisor_two_professor_three = Advisor(cross_section='Senior', orientation="computer", email=professor_three.email,
                                          time_enter_student='1397')

    user_professor_four = User(username='azimifar@gmail.com', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                               firs_name='zohreh',
                               last_name='azimifar')
    professor_four = Professor(email=user_professor_four.username)

    advisor_one_professor_four = Advisor(cross_section='masters', orientation="computer", email=professor_four.email,
                                         time_enter_student='1398')
    advisor_two_professor_four = Advisor(cross_section='Senior', orientation="artificialIntelligence",
                                         email=professor_four.email,
                                         time_enter_student='1397')

    supervisor_one_professor_four = Supervisor(cross_section='Senior', orientation="artificialIntelligence",
                                               email=professor_four.email
                                               )
    user_professor_five = User(username='Tohidi@gmail.com', password=str(hashlib.sha256("python".encode()).hexdigest()),
                               firs_name='Ahmad',
                               last_name='Tohidi')
    professor_five = Professor(email=user_professor_five.username)

    user_ResponsibleTraining_one = User(username='Parsain', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                                        firs_name='zahra',
                                        last_name='parsain')
    responsibleTraining_one = ResponsibleTraining(username=user_ResponsibleTraining_one.username,
                                                  date_start_duty=datetime(2020, 5, 17))

    user_educationAssistant_one = User(username='Hossainy', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                                       firs_name='maryam',
                                       last_name='Hossainy')
    educationAssistant_one = EducationAssistant(username=user_educationAssistant_one.username,
                                                date_start_duty=datetime(2017, 5, 17))

    session.add_all([
        user_student_one, user_student_two, user_student_three, user_student_four, user_student_five, user_student_six,
        user_student_seven,
        user_professor_one, user_professor_two, user_professor_five,
        user_professor_three, user_professor_four, user_ResponsibleTraining_one, user_educationAssistant_one
    ])
    session.add_all([student_one, student_tow, student_three, student_four, student_five, student_six, student_seven])
    session.add_all([professor_one, professor_two, professor_three, professor_four, professor_five])
    session.add_all([advisor_one_professor_one, advisor_one_professor_three, advisor_two_professor_three,
                     advisor_one_professor_four, advisor_two_professor_four])
    session.add_all([supervisor_one_professor_four, supervisor_one_professor_three, supervisor_one_professor_two])
    session.add_all([departmentHead_one_professor_two])
    session.add_all([educationAssistant_one])
    session.add_all([responsibleTraining_one])

    chart_one = Chart(educationAssistants_create_id=1, name='Test_Chart', year_create='1398')
    chart_two = Chart(educationAssistants_create_id=1, name='Test_Chart_Senior', year_create='1398')

    orientation_one = Orientation(name='ادبیات فارسی')
    orientation_two = Orientation(name='زبان خارجه')
    orientation_three = Orientation(name='فیزیک')
    orientation_four = Orientation(name='ریاضی')
    orientation_five = Orientation(name='مهندسی کامپیوتر')
    orientation_six = Orientation(name='تربیت بدنی')
    orientation_seven = Orientation(name='هوش مصنوعی ارشد')

    course_one = Course(name='فارسی عمومی', numbers_unit=3)
    course_one.orientation = orientation_one

    course_two = Course(name='انلگیسی عمومی', numbers_unit=3)
    course_two.orientation = orientation_two

    course_three = Course(name='فیزیک یک', numbers_unit=3)
    course_three.orientation = orientation_three

    course_four = Course(name='آزمایشگاه کامپیوتر', numbers_unit=1)
    course_four.orientation = orientation_five

    course_five = Course(name='ریاضی عمومی یک', numbers_unit=3)
    course_five.orientation = orientation_four

    course_six = Course(name='ساختمان گسسسته', numbers_unit=3)
    course_six.orientation = orientation_five

    course_seven = Course(name='مبانی کامپیوتر و برنامه نویسی', numbers_unit=3)
    course_seven.orientation = orientation_five

    course_eight = Course(name='اصول برنامه سازی', numbers_unit=3)
    course_eight.orientation = orientation_five

    course_nine = Course(name='مدارهای منطقی', numbers_unit=3)
    course_nine.orientation = orientation_five

    course_ten = Course(name='ریاضی عمومی ۲', numbers_unit=3)
    course_ten.orientation = orientation_four

    course_eleven = Course(name='معادلات دیفرانسیل', numbers_unit=3)
    course_eleven.orientation = orientation_four

    course_twelve = Course(name='فیزیک دو', numbers_unit=3)
    course_twelve.orientation = orientation_three

    course_thirteen = Course(name='انگلیسی تخصصی', numbers_unit=2)
    course_thirteen.orientation = orientation_two

    course_fourteen = Course(name='تربیت بدنی ۱', numbers_unit=2)
    course_fourteen.orientation = orientation_six

    course_senior_one = Course(name='هوش مصنوعی ارشد', numbers_unit=3)
    course_senior_one.orientation = orientation_seven

    preCourseLinkCourse_one = PreCourseLinkCourse(course_parent=2, course_child=13)

    preCourseLinkCourse_two = PreCourseLinkCourse(course_parent=5, course_child=12)

    preCourseLinkCourse_three = PreCourseLinkCourse(course_parent=5, course_child=11)

    preCourseLinkCourse_four = PreCourseLinkCourse(course_parent=5, course_child=10)

    preCourseLinkCourse_five = PreCourseLinkCourse(course_parent=7, course_child=8)

    NeedCourseLinkCourse_one = NeedCourseLinkCourse(first_course=3, second_course=12)

    NeedCourseLinkCourse_two = NeedCourseLinkCourse(first_course=4, second_course=6)

    NeedCourseLinkCourse_three = NeedCourseLinkCourse(first_course=4, second_course=7)

    NeedCourseLinkCourse_four = NeedCourseLinkCourse(first_course=5, second_course=6)

    NeedCourseLinkCourse_five = NeedCourseLinkCourse(first_course=6, second_course=7)

    NeedCourseLinkCourse_six = NeedCourseLinkCourse(first_course=6, second_course=9)

    session.add_all([chart_one, chart_two])
    session.add_all([course_one, course_two, course_three, course_four, course_five, course_six,
                     course_seven, course_eight, course_nine, course_ten, course_eleven, course_twelve,
                     course_thirteen, course_fourteen,course_senior_one])

    session.add_all([preCourseLinkCourse_one, preCourseLinkCourse_two, preCourseLinkCourse_three,
                     preCourseLinkCourse_four, preCourseLinkCourse_five])
    session.add_all(
        [NeedCourseLinkCourse_one, NeedCourseLinkCourse_two, NeedCourseLinkCourse_three, NeedCourseLinkCourse_four,
         NeedCourseLinkCourse_five, NeedCourseLinkCourse_six])

    chartLinkCourse_1 = ChartLinkCourse(chart_id=1, course_id=1)
    chartLinkCourse_2 = ChartLinkCourse(chart_id=1, course_id=2)
    chartLinkCourse_3 = ChartLinkCourse(chart_id=1, course_id=3)
    chartLinkCourse_4 = ChartLinkCourse(chart_id=1, course_id=4)
    chartLinkCourse_5 = ChartLinkCourse(chart_id=1, course_id=5)
    chartLinkCourse_6 = ChartLinkCourse(chart_id=1, course_id=6)
    chartLinkCourse_7 = ChartLinkCourse(chart_id=1, course_id=7)
    chartLinkCourse_8 = ChartLinkCourse(chart_id=1, course_id=8)
    chartLinkCourse_9 = ChartLinkCourse(chart_id=1, course_id=9)
    chartLinkCourse_10 = ChartLinkCourse(chart_id=1, course_id=10)
    chartLinkCourse_11 = ChartLinkCourse(chart_id=1, course_id=11)
    chartLinkCourse_12 = ChartLinkCourse(chart_id=1, course_id=12)
    chartLinkCourse_13 = ChartLinkCourse(chart_id=1, course_id=13)
    chartLinkCourse_14 = ChartLinkCourse(chart_id=1, course_id=14)
    chartLinkCourse_sinore_15 = ChartLinkCourse(chart_id=2, course_id=15)

    session.add_all([chartLinkCourse_1, chartLinkCourse_2, chartLinkCourse_3, chartLinkCourse_4, chartLinkCourse_5
                        , chartLinkCourse_6, chartLinkCourse_7, chartLinkCourse_8, chartLinkCourse_9,
                     chartLinkCourse_10, chartLinkCourse_11, chartLinkCourse_12, chartLinkCourse_13,
                     chartLinkCourse_14, chartLinkCourse_sinore_15])

    presentedCourse_one = PresentedCourse(course_id=7, year='1400', semester=Semester(1), class_name='صدری ۲',
                                          time_final_exam=str(jdatetime.date(1400, 10, 15)))
    professorLinkPresentedCourse_one = ProfessorLinkPresentedCourse(professor_email=professor_five.email,
                                                                    presentedCourse=1)

    presentedCourse_two = PresentedCourse(course_id=4, year='1400', semester=Semester(1), class_name='ICT',
                                          time_final_exam=str(jdatetime.date(1400, 10, 17)))
    professorLinkPresentedCourse_two = ProfessorLinkPresentedCourse(professor_email=professor_one.email,
                                                                    presentedCourse=7)

    presentedCourse_three = PresentedCourse(course_id=15, year='1400', semester=Semester(1),
                                            class_name='ساختمان کلاس ها ۱۳',
                                            time_final_exam=str(jdatetime.date(1400, 10, 19)))
    professorLinkPresentedCourse_three = ProfessorLinkPresentedCourse(professor_email=professor_four.email,
                                                                      presentedCourse=15)

    session.add_all([presentedCourse_one, presentedCourse_two, presentedCourse_three])
    session.add_all(
        [professorLinkPresentedCourse_one, professorLinkPresentedCourse_two, professorLinkPresentedCourse_three])
    session.commit()
    # student_student_one = Student(student_number='9732527',)


add_item_to_db()
