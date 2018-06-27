from flaskr.tests.utils import (
    create_user, login, create_course
)
import uuid


def test_get_courses(client):
    """
    Test database contains courses so at leas one should be returned.
    """
    rv = client.get('/api/courses')
    json_data = rv.get_json()
    assert rv.status == '200 OK'
    assert len(json_data['json_data']) > 0


def test_get_tickets(app, client):
    """
    Database should be empty so no tickets should be returned.
    """
    user = create_user(app, 1234)
    auth = login(client, user.id)
    course = create_course(app, courseId=uuid.uuid4(), tas=[user])
    tickets = client.get('/api/courses/{}/tickets'.format(course.id),
                         headers={'Authorization': auth})

    assert tickets.status == '200 OK'
    print(tickets.get_json())
    assert len(tickets.get_json()['json_data']) == 0


def test_incorrect_course_post(client):
    """
    Not sending any json should return 400.
    """
    rv = client.post('/api/courses')
    assert rv.status == '400 BAD REQUEST'


def test_insert_ticket(app, client):
    """
    Insert a new ticket.
    """
    create_user(app, 11188936)
    auth = login(client, 11188936)
    rv = client.get('/api/courses', headers={
        'Authorization': auth
    })
    cid = rv.get_json()['json_data'][0]['id']
    print("course: {}".format(cid))

    rv = client.post('/api/ticket/submit', json={
            'subject': 'test ticket',
            'message': 'Test bericht',
            'courseid': cid,
            'labelid': '',
            'files': ''
    }, headers={
        'Authorization': auth
    })
    print(rv.data)
    assert rv.status == '201 CREATED'


def test_get_ticket(app, client):
    user = create_user(app, 11188936)
    auth = login(client, 11188936)
    course = create_course(app, uuid.uuid4(), tas=[user])
    rv = client.post('/api/ticket/submit', json={
        'subject': 'test ticket',
        'message': 'Test bericht',
        'courseid': course.id,
        'labelid': ''
    }, headers={
        'Authorization': auth
    })
    tickets = client.get('/api/courses/{}/tickets'.format(course.id),
                         headers={
                             'Authorization': auth
                         })

    print(tickets.get_json())
    assert len(tickets.get_json()['json_data']) == 1
    ticketid = tickets.get_json()['json_data'][0]['id']
    assert ticketid is not None
