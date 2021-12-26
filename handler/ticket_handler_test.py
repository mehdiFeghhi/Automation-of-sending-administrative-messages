import requests
from itsdangerous import json


def create_ticket_test(type_create, token, course_id, description, subject, receiver_id, status):
    url = f"http://127.0.0.1:5000/api/{type_create}"

    payload = json.dumps({
        "receiver_id": f"{receiver_id}",
        "subject": f"{subject}",
        "description": f"{description}",
        "course_id": f"{course_id}"
    })
    headers = {
        '': '',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    assert json.loads(response.json()).get('Status') == status


def get_ticket_test(token, status):
    url = "http://127.0.0.1:5000/api/get-courses"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    assert json.loads(response.json()).get('Status') == status


def add_step_to_ticket_test(token, id_ticket, message, step, url_file, status):
    url = "http://127.0.0.1:5000/step-ticket"

    payload = json.dumps({
        "step": f"{step}",
        "massage": f"{message}",
        "id_ticket": id_ticket,
        "url": f'{url_file}'
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    assert json.loads(response.json()).get('Status') == status


def delete_step_ticket_test(token, id_ticket, status):
    url = "http://127.0.0.1:5000/api/step-ticket"

    payload = json.dumps({
        "id_ticket": id_ticket
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    assert json.loads(response.json()).get('Status') == status


