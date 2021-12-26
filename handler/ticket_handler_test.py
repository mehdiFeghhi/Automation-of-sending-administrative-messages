import requests
from itsdangerous import json


def create_ticket_test(type_create,token):
    url = f"http://127.0.0.1:5000/{type_create}"

    payload = json.dumps({
        "receiver_id": "any thing can be back handler it",
        "subject": "capacity_increase",
        "description": "",
        "course_id": "7"
    })
    headers = {
        '': '',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
