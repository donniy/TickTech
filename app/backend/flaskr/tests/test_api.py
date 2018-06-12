import pytest
import json
from flaskr.database import get_db

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

def test_course_post(client):
    """
    Try inserting a new course.
    """
    rv = client.post('/api/courses', json={
        'title': 'Test course',
        'mail': 'test.testerson@student.uva.nl',
        'description': 'test description'
    })
    assert rv.status == 'asdf'
