import hashlib
import os
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from config import db
from handler.model.modelDB import *
from app import app


# file_path = os.path.abspath(os.getcwd()) + "/sample.db"
# engine = create_engine('sqlite:///' + file_path, echo=True)
#
# Session = sessionmaker(bind=engine)
# session = Session()

charts = [
    {
        'name': 'کارشناسی',
        'year_create': '97'
    },
    {
        'name': 'کارشناسی',
        'year_create': '98'
    },
    {
        'name': 'کارشناسی',
        'year_create': '99'
    },
    {
        'name': 'کارشناسی',
        'year_create': '00'
    },

]

courses = [
    {
        'numbers_unit': int(1),
        'orientation_id': int(1),
        'name': 'آزمایشگاه کامپیوتر',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'ساختمان گسسته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'مبانی کامپیوتر و برنامه‌نویسی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'مدارهای منطقی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'اصول برنامه‌سازی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'مدار‌های الکتریکی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'ریاضی مهندسی',
    },
    {
        'numbers_unit': int(1),
        'orientation_id': int(1),
        'name': 'آز مدارهای منطقی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'زبان ماشین و برنامه‌سازی سیستم',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'برنامه‌سازی پیشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'روش‌های محاسبات عددی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'مدار‌های الکترونیکی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'معماری کامپیوتر',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'ساختمان داده‌ها و الگوریتم‌ها',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'نظریه زبان‌ها و ماشین',
    },
    {
        'numbers_unit': int(2),
        'orientation_id': int(1),
        'name': 'شیوه ارائه مطالب علمی و فنی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'سیگنال‌ها و سیستم‌ها',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'اصول طراحی سیستم‌های عامل',
    },
    {
        'numbers_unit': int(1),
        'orientation_id': int(1),
        'name': 'آز معماری کامپیوتر',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'طراحی و تحلیل الگوریتم‌ها',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'انتقال داده‌ها',
    },
    {
        'numbers_unit': int(1),
        'orientation_id': int(1),
        'name': 'آزمایشگاه سیستم‌های عامل',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'ریزپردازنده',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'اصول طراحی پایگاه داده‌ها',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'هوش مصنوعی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'شبکه‌های کامپیوتری',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'طراحی کامپیوتری سیستم‌های دیجیتال',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'تحلیل و طراحی سیستم‌ها',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'اصول طراحی کامپایلر‌ها',
    },
    {
        'numbers_unit': int(1),
        'orientation_id': int(1),
        'name': 'آز ریزپردازنده',
    },
    {
        'numbers_unit': int(1),
        'orientation_id': int(1),
        'name': 'آز شبکه‌های کامپیوتری',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'پروژه کارشناسی',
    },
    {
        'numbers_unit': int(2),
        'orientation_id': int(6),
        'name': 'کارآموزی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(3),
        'name': 'ریاضیات عمومی ۱',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(5),
        'name': 'فیزیک یک',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(3),
        'name': 'ریاضیات عمومی ۲',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(5),
        'name': 'فیزیک دو',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(3),
        'name': 'معادلات دیفرانسیل',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(2),
        'name': 'انگلیسی عمومی معافی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(2),
        'name': 'انگلیسی تخصصی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(1),
        'name': 'آمار و احتمال مهندسی',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'سیستم‌های عامل پیشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'سیستم‌های عامل پیشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'پايگاه داده پيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'مهندسي نرم افزار پيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'الگوريتم هاي موازي',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'رياضيات پيشرفته درمهندسي كامپيوتر',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'طراحي الگوريتمهاي پيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'داده كاوي',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'مدلسازي و ارزيابي',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'معماري نرم افزار',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'رياضيات پيشرفته در مهندسي كامپيوتر',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(8),
        'name': 'پردازش تكاملي',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(8),
        'name': 'يادگيري ماشين',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(8),
        'name': 'پردازش نمادي',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(8),
        'name': 'شبكه عصبي و يادگيري عميق',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(8),
        'name': 'هوش مصنوعي پيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(8),
        'name': 'رياضيات مهندسي پيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(9),
        'name': 'سيستم هاي اطلاعات مديريت',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(9),
        'name': 'مديريت دانش',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(9),
        'name': 'معماري سازماني فناوري اطلاعات',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(9),
        'name': 'معماري اطلاعات',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(9),
        'name': 'مديريت فناوري اطلاعات',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(9),
        'name': 'محاسبات علمي و تحليل داده',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'آزمون و آزمون پذيري سخت افزار',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'طراحي سيستمهاي تحمل پذير اشكال',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'ريزپردازنده هاي پيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(7),
        'name': 'شبكه هاي كامپيوتري پيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'طراحي مدارهاي مجتمع پيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'معماري هاي قابل باز پيكربندي',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'سیستم‌های عامل پیشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'پردازش موازي',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'معماري كامپيوترپيشرفته',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(10),
        'name': 'الگوريتم هاي موازي',
    },

    {
        'numbers_unit': int(3),
        'orientation_id': int(11),
        'name': 'توسعه امن نرم افزار',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(11),
        'name': 'امنيت شبکه',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(11),
        'name': 'مباني امنيت اطلاعات',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(11),
        'name': 'امنيت پايگاه داده',
    },
    {
        'numbers_unit': int(3),
        'orientation_id': int(11),
        'name': 'رياضيات رمز نگاري',
    },

]

pre_courses = [
    {
        'course_parent': 'ریاضیات عمومی ۱',
        'course_child': 'ریاضیات عمومی ۲'
    },
    {
        'course_parent': 'ریاضیات عمومی ۱',
        'course_child': 'معادلات دیفرانسیل'
    },
    {
        'course_parent': 'ریاضیات عمومی ۱',
        'course_child': 'فیزیک دو'
    },
    {
        'course_parent': 'مبانی کامپیوتر و برنامه‌نویسی',
        'course_child': 'اصول برنامه‌سازی'
    },
    {
        'course_parent': 'انگلیسی عمومی معافی',
        'course_child': 'انگلیسی تخصصی'
    },
    {
        'course_parent': 'اصول برنامه‌سازی',
        'course_child': 'برنامه‌سازی پیشرفته'
    },
    {
        'course_parent': 'ساختمان گسسته',
        'course_child': 'برنامه‌سازی پیشرفته'
    },
    {
        'course_parent': 'معادلات دیفرانسیل',
        'course_child': 'ریاضی مهندسی'
    },
    {
        'course_parent': 'معادلات دیفرانسیل',
        'course_child': 'مدار‌های الکتریکی'
    },
    {
        'course_parent': 'انگلیسی تخصصی',
        'course_child': 'شیوه ارائه مطالب علمی و فنی'
    },
    {
        'course_parent': 'اصول برنامه‌سازی',
        'course_child': 'زبان ماشین و برنامه‌سازی سیستم'
    },
    {
        'course_parent': 'مدارهای منطقی',
        'course_child': 'آز مدارهای منطقی'
    },
    {
        'course_parent': 'ریاضیات عمومی ۲',
        'course_child': 'آمار و احتمال مهندسی'
    },
    {
        'course_parent': 'ریاضیات عمومی ۲',
        'course_child': 'ریاضی مهندسی'
    },
    {
        'course_parent': 'برنامه‌سازی پیشرفته',
        'course_child': 'ساختمان داده‌ها و الگوریتم‌ها'
    },
    {
        'course_parent': 'اصول برنامه‌سازی',
        'course_child': 'نظریه زبان‌ها و ماشین'
    },
    {
        'course_parent': 'مدارهای منطقی',
        'course_child': 'معماری کامپیوتر'
    },
    {
        'course_parent': 'زبان ماشین و برنامه‌سازی سیستم',
        'course_child': 'معماری کامپیوتر'
    },
    {
        'course_parent': 'مدار‌های الکتریکی',
        'course_child': 'مدار‌های الکترونیکی'
    },
    {
        'course_parent': 'ساختمان داده‌ها و الگوریتم‌ها',
        'course_child': 'طراحی و تحلیل الگوریتم‌ها'
    },
    {
        'course_parent': 'معماری کامپیوتر',
        'course_child': 'آز معماری کامپیوتر'
    },
    {
        'course_parent': 'معماری کامپیوتر',
        'course_child': 'اصول طراحی سیستم‌های عامل'
    },
    {
        'course_parent': 'ریاضی مهندسی',
        'course_child': 'سیگنال‌ها و سیستم‌ها'
    },
    {
        'course_parent': 'ساختمان داده‌ها و الگوریتم‌ها',
        'course_child': 'اصول طراحی پایگاه داده‌ها'
    },
    {
        'course_parent': 'معماری کامپیوتر',
        'course_child': 'ریزپردازنده'
    },
    {
        'course_parent': 'اصول طراحی سیستم‌های عامل',
        'course_child': 'آزمایشگاه سیستم‌های عامل'
    },
    {
        'course_parent': 'آمار و احتمال مهندسی',
        'course_child': 'انتقال داده‌ها'
    },
    {
        'course_parent': 'سیگنال‌ها و سیستم‌ها',
        'course_child': 'انتقال داده‌ها'
    },
    {
        'course_parent': 'نظریه زبان‌ها و ماشین',
        'course_child': 'اصول طراحی کامپایلر‌ها'
    },
    {
        'course_parent': 'ریزپردازنده',
        'course_child': 'آز ریزپردازنده'
    },
    {
        'course_parent': 'معماری کامپیوتر',
        'course_child': 'طراحی کامپیوتری سیستم‌های دیجیتال'
    },
    {
        'course_parent': 'انتقال داده‌ها',
        'course_child': 'شبکه‌های کامپیوتری'
    },
    {
        'course_parent': 'شیوه ارائه مطالب علمی و فنی',
        'course_child': 'پروژه کارشناسی'
    },
    {
        'course_parent': 'شیوه ارائه مطالب علمی و فنی',
        'course_child': 'کارآموزی'
    },
    {
        'course_parent': 'شبکه‌های کامپیوتری',
        'course_child': 'آز شبکه‌های کامپیوتری'
    },
]

need_courses = [
    {
        'first_course': 'مبانی کامپیوتر و برنامه‌نویسی',
        'second_course': 'ساختمان گسسته'
    },
    {
        'first_course': 'مبانی کامپیوتر و برنامه‌نویسی',
        'second_course': 'آزمایشگاه کامپیوتر'
    },
    {
        'first_course': 'فیزیک یک',
        'second_course': 'فیزیک دو'
    },
    {
        'first_course': 'ساختمان گسسته',
        'second_course': 'مدارهای منطقی'
    },
    {
        'first_course': 'ساختمان گسسته',
        'second_course': 'برنامه‌سازی پیشرفته'
    },
    {
        'first_course': 'معادلات دیفرانسیل',
        'second_course': 'روش‌های محاسبات عددی'
    },
    {
        'first_course': 'طراحی و تحلیل الگوریتم‌ها',
        'second_course': 'هوش مصنوعی'
    },
    {
        'first_course': 'اصول طراحی پایگاه داده‌ها',
        'second_course': 'تحلیل و طراحی سیستم‌ها'
    },
]


def init_charts():
    for chart in charts:
        if not Chart.query.filter_by(**chart).one_or_none():
            model = Chart(**chart)
            db.session.add(model)

    db.session.commit()


def init_courses():
    for course in courses:
        if not Course.query.filter_by(**course).one_or_none():
            model = Course(**course)
            db.session.add(model)

    db.session.commit()


def init_course_link_chart():
    charts = Chart.query.filter_by(name='کارشناسی')
    courses = Course.query.all()
    for chart in charts:
        for course in courses:
            if not ChartLinkCourse.query.filter_by(chart_id=chart.id, course_id=course.id).one_or_none():
                chart_link = ChartLinkCourse(
                    chart_id=chart.id, course_id=course.id)
                db.session.add(chart_link)

    db.session.commit()


def init_pre_course():
    for pre_course in pre_courses:

        parent_course = Course.query.filter_by(
            name=pre_course.get('course_parent')).one()
        child_course = Course.query.filter_by(
            name=pre_course.get('course_child')).one()
        if not PreCourseLinkCourse.query.filter_by(course_parent=parent_course.id,
                                                   course_child=child_course.id).one_or_none():
            model = PreCourseLinkCourse(course_parent=parent_course.id,
                                        course_child=child_course.id)

            db.session.add(model)

    db.session.commit()


def init_need_course():
    for need_course in need_courses:
        # print(
        #     f'first_course: {need_course.get("first_course")} , second_course: {need_course.get("second_course")}')
        first_course = Course.query.filter_by(
            name=need_course.get('first_course')).one()
        second_course = Course.query.filter_by(
            name=need_course.get('second_course')).one()
        if not NeedCourseLinkCourse.query.filter_by(first_course=first_course.id,
                                                    second_course=second_course.id).one_or_none():
            model = NeedCourseLinkCourse(first_course=first_course.id,
                                         second_course=second_course.id)

            db.session.add(model)

    db.session.commit()


def init_db():
    orientation_one = Orientation(name='مهندسی کامپیوتر')
    orientation_two = Orientation(name='زبان خارج')
    orientation_three = Orientation(name='ریاضیات کارشناسی')
    orientation_four = Orientation(name='تربیت بدنی')
    orientation_five = Orientation(name='فیزیک کارشناسی')
    orientation_six = Orientation(name='مدیریت')
    orientation_seven = Orientation(name='ارشد نرم افزار')
    orientation_eight = Orientation(name='ارشد هوش مصنوعی')
    orientation_nine = Orientation(name=' ارشد فناوری اطلاعات- مدیریت سیستم')
    orientation_ten = Orientation(name='ارشد معماری کامپیوتر')
    orientation_eleven = Orientation(name='ارشد رایانش امن')

    db.create_all()

    db.session.add(orientation_one)
    db.session.add(orientation_two)
    db.session.add(orientation_three)
    db.session.add(orientation_four)
    db.session.add(orientation_five)
    db.session.add(orientation_six)
    db.session.add(orientation_seven)
    db.session.add(orientation_eight)
    db.session.add(orientation_nine)
    db.session.add(orientation_ten)
    db.session.add(orientation_eleven)


    db.session.commit()

    init_charts()
    init_courses()
    init_course_link_chart()
    init_pre_course()
    init_need_course()

    user_educationAssistant_one = User(username='Hossainy', password=str(hashlib.sha256("4231".encode()).hexdigest()),
                                       firs_name='زهرا',
                                       last_name='حسینی')
    educationAssistant_one = EducationAssistant(username=user_educationAssistant_one.username,
                                                date_start_duty=datetime(2021, 5, 17))
    db.session.add(user_educationAssistant_one)
    db.session.add(educationAssistant_one)

    db.session.commit()

