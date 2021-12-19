import unittest

from user_handler import find_user_by_username_and_password
import pprint


def test_find_user_by_username_and_password(user_name, password, status):
    data = find_user_by_username_and_password(user_name, password)
    pprint.pprint(data)

    assert data.get('Status') == status


if __name__ == '__main__':
    test_find_user_by_username_and_password('9732527', '1234', 'OK')
    test_find_user_by_username_and_password('sami@gmail.com', '4231', 'OK')
    test_find_user_by_username_and_password('Parsain', '4231', 'OK')
    test_find_user_by_username_and_password('Hossainy', '4231', 'OK')