import pytest
from flaskr.database import get_db

def test_get_courses(client):
    rv = client.get('/api/courses')
    json_data = rv.get_json()
    assert rv.status == '200 OK'
    assert len(json_data['json_data']) > 0

def test_get_tickets(client):
    rv = client.get('/api/courses')
    cid = rv.get_json()['json_data'][0]['id']
    tickets = client.get('/api/courses/{}/tickets'.format(cid))
    assert tickets.status == '200 OK'
    print(tickets.get_json())
    assert len(tickets.get_json()['json_data']) > 0
