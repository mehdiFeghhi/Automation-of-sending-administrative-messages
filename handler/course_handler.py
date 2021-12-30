from sqlalchemy import and_, or_

from handler.model.modelDB import Student, Course, Professor, PresentedCourse, Semester, PreCourseLinkCourse, \
    ProfessorLinkPresentedCourse, Ticket, Step, EducationAssistant, User, StatusStep, DepartmentHead, Advisor, Supervisor, Orientation
from handler.connect_db import session
import jdatetime

def get_course_list():
  courses = session.query(Course).all()
  res = []
  for course in courses:
    orient_list = []
    # print(course.orientation)
    for orient in session.query(Orientation).filter(Orientation.id == course.orientation_id).all():
      orient_list.append({"id_course": course.id, "name_orientation": orient.name})

    course_info = {"course": course.name, "list_orientation": orient_list}
    res.append(course_info)

  return res

def get_orientations_handler():
  res = []
  orientation_list = Orientation.query.all()
  for orientation in orientation_list:
    print(orientation.name)
    res.append({
      "id": orientation.id,
      "name": orientation.name
    })
  return res
  
def create_course_handler(user_id, name_course, orientation_id, unit_numbers, prerequisites):
  if(session.query(EducationAssistant).filter(EducationAssistant.username == user_id).first() != None):
    new_course = Course(name = name_course,
                      numbers_unit = unit_numbers,
                      orientation_id = orientation_id)

    session.add(new_course)
    session.commit()
    for preq in prerequisites:
      new_preq = PreCourseLinkCourse(course_parent = preq, course_child = new_course.id)
      session.add(new_preq)
    
    session.commit()
    return {'Status': 'OK'}
  
  else:
    return {'Status': 'شما مجوز انجام اینکار را ندارید'}
  
