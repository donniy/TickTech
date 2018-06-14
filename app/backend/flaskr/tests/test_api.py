import pytest
import json
from flaskr.database import get_db
from flaskr.models.user import *
from flaskr.models.ticket import *
from flaskr.tests.test_user import *


def test_get_courses(client):
    """
    Test database contains courses so at leas one should be returned.
    """
    rv = client.get('/api/courses')
    json_data = rv.get_json()
    assert rv.status == '200 OK'
    assert len(json_data['json_data']) > 0


def test_get_tickets(client):
    """
    Database should be empty so no tickets should be returned.
    """
    rv = client.get('/api/courses')
    cid = rv.get_json()['json_data'][0]['id']
    tickets = client.get('/api/courses/{}/tickets'.format(cid))
    assert tickets.status == '200 OK'
    print(tickets.get_json())
    assert len(tickets.get_json()['json_data']) == 0


def test_incorrect_course_post(client):
    """
    Not sending any json should return 400.
    """
    rv = client.post('/api/courses')
    assert rv.status == '400 BAD REQUEST'


def test_insert_ticket(client):
    """
    Insert a new ticket.
    """
    rv = client.get('/api/courses')
    cid = rv.get_json()['json_data'][0]['id']
    rv = client.post('/api/ticket/submit', json={
        'studentid': '111111',
        'name': 'Piet Pietersen',
        'email': 'piet.pietersen@student.uva.nl',
        'subject': 'test ticket',
        'message': 'Test bericht',
        'courseid': cid,
        'labelid': ''
    })
    assert rv.status == '201 CREATED'


def test_get_ticket(client):
    rv = client.get('/api/courses')
    cid = rv.get_json()['json_data'][0]['id']
    rv = client.post('/api/ticket/submit', json={
        'studentid': '111111',
        'name': 'Piet Pietersen',
        'email': 'piet.pietersen@student.uva.nl',
        'subject': 'test ticket',
        'message': 'Test bericht',
        'courseid': cid,
        'labelid': ''
    })
    rv = client.get('/api/courses')
    cid = rv.get_json()['json_data'][0]['id']
    tickets = client.get('/api/courses/{}/tickets'.format(cid))
    print(tickets.get_json())
    assert len(tickets.get_json()['json_data']) == 1
    ticketid = tickets.get_json()['json_data'][0]['id']
    assert ticketid is not None


def test_db_acces(app):
    user1 = create_user(app, 1111)
    print(user1.name)
