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
        'name': 'مدار منطقی',
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
        'name': '‌مدار‌های الکترونیکی',
    },
    {
        'numbers_unit': int(3),
        'name': 'معماری کامپیوتر',
    },
    {
        'numbers_unit': int(3),
        'name': 'ساختمان داده‌های و الگوریتم‌ها',
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
        'name': 'اصول سیستم‌های عامل',
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


def init_db():
    db.create_all()
    init_charts()
    init_courses()
    init_course_link_chart()
