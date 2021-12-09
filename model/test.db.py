from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib

from model.modelDB import User, Student, Advisor, Professor, Supervisor, DepartmentHead, EducationAssistant, \
    ResponsibleTraining

engine = create_engine('sqlite:///sample.db', echo=True)

Session = sessionmaker(bind=engine)


def add_item_to_db():
    session = Session()
    user_student_one = User(username='9732527', password=str(hashlib.sha256("1234".encode())),
                            firs_name='mehdi',
                            last_name='Feghhi')
    student_one = Student(student_number=user_student_one.username, time_enter='1397', cross_section='masters',
                          orientation='computer')
    # user_student_one.student = student_one

    # add mehdi to data base as student

    user_student_two = User(username='9632527', password=str(hashlib.sha256("1234".encode())),
                            firs_name='hassan',
                            last_name='Abbasi')
    student_tow = Student(student_number=user_student_two.username, time_enter='1396', cross_section='masters',
                          orientation='computer')
    # user_student_two.student = student_tow
    # add hassan to data base as student

    user_student_three = User(username='9732557', password=str(hashlib.sha256("1234".encode())),
                              firs_name='poay',
                              last_name='fekry')
    student_three = Student(student_number=user_student_three.username, time_enter='1397', cross_section='masters',
                            orientation='computer')
    # user_student_three.student = student_three
    # add hassan to data base as student

    user_student_four = User(username='9832538', password=str(hashlib.sha256("1234".encode())),
                             firs_name='reza',
                             last_name='farjam')
    student_four = Student(student_number=user_student_four.username, time_enter='1398', cross_section='masters',
                           orientation='computer')
    # user_student_four.student = student_four

    user_student_five = User(username='9732517', password=str(hashlib.sha256("4231".encode())),
                             firs_name='mood',
                             last_name='sharizi')
    student_five = Student(student_number=user_student_five.username, time_enter='1397', cross_section='masters',
                           orientation='computer')
    # user_student_five.student = student_five

    user_student_six = User(username='9732527', password=str(hashlib.sha256("4231".encode())),
                            firs_name='hossain',
                            last_name='hedayadtzadeh')
    student_six = Student(student_number=user_student_six.username, time_enter='1397', cross_section='senior',
                          orientation='computer')
    # user_student_six.student = student_six

    user_student_seven = User(username='9822528', password=str(hashlib.sha256("4231".encode())),
                              firs_name='sara',
                              last_name='mohammady')
    student_seven = Student(student_number=user_student_seven.username, time_enter='1398', cross_section='senior',
                            orientation='computer')
    # user_student_seven.student = student_seven

    user_professor_one = User(username='keshtkaran@gmail.com', password=str(hashlib.sha256("4231".encode())),
                              firs_name='morteza',
                              last_name='keshtkaran')
    professor_one = Professor(email=user_professor_one.username)

    advisor_one_professor_one = Advisor(cross_section='masters', orientation="computer", email=professor_one.email,
                                        time_enter_student="1397")
    # professor_one.advisors.append(advisor_one_professor_one)
    advisor_one_professor_one.professor = professor_one

    user_professor_two = User(username='sami@gmail.com', password=str(hashlib.sha256("4231".encode())),
                              firs_name='ashkan',
                              last_name='sami')
    professor_two = Professor(email=user_professor_two.username)

    supervisor_one_professor_two = Supervisor(cross_section='Senior', orientation="artificialIntelligence",
                                              email=professor_two.email,
                                              )
    supervisor_one_professor_two.professor = professor_two
    # professor_two.supervisor.append(supervisor_one_professor_two)
    departmentHead_one_professor_two = DepartmentHead(email=professor_two.email,
                                                      date_start_duty=datetime(2019, 5, 17))
    departmentHead_one_professor_two.professor = professor_two
    # professor_two.departmentHeads.append(departmentHead_one_professor_two)

    user_professor_three = User(username='taheri@gmail.com', password=str(hashlib.sha256("4231".encode())),
                                firs_name='mohammdad',
                                last_name='taheri')
    professor_three = Professor(email=user_professor_three.username)
    supervisor_one_professor_three = Supervisor(cross_section='Senior', orientation="artificialIntelligence",
                                                email=professor_three.email,
                                                )
    supervisor_one_professor_three.professor = professor_three
    # professor_two.supervisor.append(supervisor_one_professor_three)

    student_six.supervisor_id = supervisor_one_professor_three.id
    supervisor_one_professor_three.students.append(student_six)

    advisor_one_professor_three = Advisor(cross_section='masters', orientation="computer", email=professor_three.email,
                                          time_enter_student='1396')
    advisor_one_professor_three.professor = professor_three
    # professor_three.advisors.append(advisor_one_professor_three)

    advisor_two_professor_three = Advisor(cross_section='Senior', orientation="computer", email=professor_three.email,
                                          time_enter_student='1397')
    advisor_two_professor_three.professor = professor_three
    # professor_three.advisors.append(advisor_two_professor_three)

    user_professor_four = User(username='azimifar@gmail.com', password=str(hashlib.sha256("4231".encode())),
                               firs_name='zohreh',
                               last_name='azimifar')
    professor_four = Professor(email=user_professor_four.username)
    advisor_one_professor_four = Advisor(cross_section='masters', orientation="computer", email=professor_three.email,
                                         time_enter_student='1398')
    advisor_one_professor_four.professor = professor_four
    advisor_two_professor_four = Advisor(cross_section='Senior', orientation="artificialIntelligence",
                                         email=professor_three.email,
                                         time_enter_student='1397')
    advisor_two_professor_four.professor = professor_four

    supervisor_one_professor_four = Supervisor(cross_section='Senior', orientation="artificialIntelligence",
                                               email=professor_four.email
                                               )
    # professor_four.supervisor.apeend(supervisor_one_professor_four)
    supervisor_one_professor_four.professor = professor_four
    # professor_four.advisors.append(advisor_one_professor_four)
    # professor_four.advisors.append(advisor_two_professor_four)

    user_ResponsibleTraining_one = User(username='Parsain', password=str(hashlib.sha256("4231".encode())),
                                        firs_name='zahra',
                                        last_name='parsain')
    responsibleTraining_one = ResponsibleTraining(username=user_ResponsibleTraining_one.username,
                                                  date_start_duty=datetime(2020, 5, 17))
    responsibleTraining_one.user = user_ResponsibleTraining_one
    # user_ResponsibleTraining_one.responsibleTrainings.append(responsibleTraining_one)

    user_educationAssistant_one = User(username='Hossainy', password=str(hashlib.sha256("4231".encode())),
                                       firs_name='maryam',
                                       last_name='Hossainy')
    educationAssistant_one = EducationAssistant(username=user_educationAssistant_one.username,
                                                date_start_duty=datetime(2017, 5, 17))
    educationAssistant_one.user = user_educationAssistant_one
    # educationAssistant_one.educationAssistants.append(educationAssistant_one)

    session.add_all([
        user_student_one, user_student_two, user_student_three, user_student_four, user_student_five,
        user_professor_one, user_professor_two,
        user_professor_three, user_professor_four, user_ResponsibleTraining_one, user_educationAssistant_one
    ])
    # session.add_all([student_one, student_tow, student_three, student_four, student_five, student_six])
    # session.add_all([professor_one, professor_two, professor_three, professor_four])
    # session.add_all([advisor_one_professor_one, advisor_one_professor_three, advisor_two_professor_three,
    #                  advisor_one_professor_four, advisor_two_professor_four])
    # session.add_all([supervisor_one_professor_four, supervisor_one_professor_three, supervisor_one_professor_two])
    # session.add_all([departmentHead_one_professor_two])
    session.commit()
    # student_student_one = Student(student_number='9732527',)


add_item_to_db()
