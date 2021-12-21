from sqlalchemy import and_, or_

from handler.model.modelDB import Student, Course, Professor, PresentedCourse, Semester, PreCourseLinkCourse, \
    ProfessorLinkPresentedCourse, Ticket, Step, EducationAssistant, User, StatusStep, DepartmentHead, Advisor, Orientation
from handler.connect_db import session
import jdatetime

def get_course_list():
  courses = session.query(Course).all();
  res = []
  for course in courses:
    orient_list = []
    # print(course.orientation)
    for orient in session.query(Orientation).filter(Orientation.id == course.orientation_id).all():
      orient_list.append({"id_course": course.id, "name_orientation": orient.name})

    course_info = {"course": course.name, "list_orientation": orient_list}
    res.append(course_info)

  return res