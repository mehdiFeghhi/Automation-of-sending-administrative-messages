from handler.cours_selection import is_this_course_exist


def test_is_this_course_exist(course_id, status_bool):
    assert is_this_course_exist(course_id) == status_bool


if __name__ == '__main__':
    test_is_this_course_exist(20, True)
    test_is_this_course_exist(1, True)

