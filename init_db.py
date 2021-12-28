from config import db
from handler.model.modelDB import *
from app import app

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
        'name': 'آزمایشگاه کامپیوتر',
    },
    {
        'numbers_unit': int(3),
        'name': 'ساختمان گسسته',
    },
    {
        'numbers_unit': int(3),
        'name': 'مبانی کامپیوتر و برنامه‌نویسی',
    },
    {
        'numbers_unit': int(3),
        'name': 'مدارهای منطقی',
    },
    {
        'numbers_unit': int(3),
        'name': 'اصول برنامه‌سازی',
    },
    {
        'numbers_unit': int(3),
        'name': 'مدار‌های الکتریکی',
    },
    {
        'numbers_unit': int(3),
        'name': 'ریاضی مهندسی',
    },
    {
        'numbers_unit': int(1),
        'name': 'آز مدارهای منطقی',
    },
    {
        'numbers_unit': int(3),
        'name': 'زبان ماشین و برنامه‌سازی سیستم',
    },
    {
        'numbers_unit': int(3),
        'name': 'برنامه‌سازی پیشرفته',
    },
    {
        'numbers_unit': int(3),
        'name': 'روش‌های محاسبات عددی',
    },
    {
        'numbers_unit': int(3),
        'name': 'مدار‌های الکترونیکی',
    },
    {
        'numbers_unit': int(3),
        'name': 'معماری کامپیوتر',
    },
    {
        'numbers_unit': int(3),
        'name': 'ساختمان داده‌ها و الگوریتم‌ها',
    },
    {
        'numbers_unit': int(3),
        'name': 'نظریه زبان‌ها و ماشین',
    },
    {
        'numbers_unit': int(2),
        'name': 'شیوه ارائه مطالب علمی و فنی',
    },
    {
        'numbers_unit': int(3),
        'name': 'سیگنال‌ها و سیستم‌ها',
    },
    {
        'numbers_unit': int(3),
        'name': 'اصول طراحی سیستم‌های عامل',
    },
    {
        'numbers_unit': int(1),
        'name': 'آز معماری کامپیوتر',
    },
    {
        'numbers_unit': int(3),
        'name': 'طراحی و تحلیل الگوریتم‌ها',
    },
    {
        'numbers_unit': int(3),
        'name': 'انتقال داده‌ها',
    },
    {
        'numbers_unit': int(1),
        'name': 'آزمایشگاه سیستم‌های عامل',
    },
    {
        'numbers_unit': int(3),
        'name': 'ریزپردازنده',
    },
    {
        'numbers_unit': int(3),
        'name': 'اصول طراحی پایگاه داده‌ها',
    },
    {
        'numbers_unit': int(3),
        'name': 'هوش مصنوعی',
    },
    {
        'numbers_unit': int(3),
        'name': 'شبکه‌های کامپیوتری',
    },
    {
        'numbers_unit': int(3),
        'name': 'طراحی کامپیوتری سیستم‌های دیجیتال',
    },
    {
        'numbers_unit': int(3),
        'name': 'تحلیل و طراحی سیستم‌ها',
    },
    {
        'numbers_unit': int(3),
        'name': 'اصول طراحی کامپایلر‌ها',
    },
    {
        'numbers_unit': int(1),
        'name': 'آز ریزپردازنده',
    },
    {
        'numbers_unit': int(1),
        'name': 'آز شبکه‌های کامپیوتری',
    },
    {
        'numbers_unit': int(3),
        'name': 'پروژه کارشناسی',
    },
    {
        'numbers_unit': int(2),
        'name': 'کارآموزی',
    },
    {
        'numbers_unit': int(3),
        'name': 'ریاضیات عمومی ۱',
    },
    {
        'numbers_unit': int(3),
        'name': 'فیزیک یک',
    },
    {
        'numbers_unit': int(3),
        'name': 'ریاضیات عمومی ۲',
    },
    {
        'numbers_unit': int(3),
        'name': 'فیزیک دو',
    },
    {
        'numbers_unit': int(3),
        'name': 'معادلات دیفرانسیل',
    },
    {
        'numbers_unit': int(3),
        'name': 'انگلیسی عمومی معافی',
    },
    {
        'numbers_unit': int(3),
        'name': 'انگلیسی تخصصی',
    },
    {
        'numbers_unit': int(3),
        'name': 'آمار و احتمال مهندسی',
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
        # print(f'parent_course: {pre_course.get("course_parent")} , child_course: {pre_course.get("course_child")}' )
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
    db.create_all()
    init_charts()
    init_courses()
    init_course_link_chart()
    init_pre_course()
    init_need_course()
