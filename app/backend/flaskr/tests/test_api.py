from flaskr.tests.utils import create_user, login, create_course,\
        link_ta_to_course, link_student_to_course, link_supervisor_to_course
import uuid


def test_get_courses(app, client):
    """
    Test database contains courses so at leas one should be returned.
    """
    usr = create_user(app, 12345)
    c = create_course(app, uuid.uuid4())
    link_ta_to_course(usr, c)
    auth = login(client, usr.id)
    rv = client.get('/api/courses',
                    headers={'Authorization': auth})
    json_data = rv.get_json()
    assert rv.status == '200 OK'
    assert len(json_data['json_data']) > 0


def test_get_tickets(app, client):
    """
    Database should be empty so no tickets should be returned.
    """
    usr = create_user(app, 12345)
    auth = login(client, usr.id)
    c = create_course(app, courseId=uuid.uuid4(), tas=[usr])
    tickets = client.get('/api/courses/{}/tickets'.format(c.id),
                         headers={'Authorization': auth})
    assert tickets.status == '200 OK'
    print(tickets.get_json())
    assert len(tickets.get_json()['json_data']) == 0


def test_incorrect_course_post(app, client):
    """
    Not sending any json should return 400.
    """
    usr = create_user(app, 12345)
    c = create_course(app, uuid.uuid4(), supervisors=[usr])
    # link_supervisor_to_course(usr, c)
    auth = login(client, usr.id)
    rv = client.post('/api/courses',
                     headers={'Authorization': auth})
    assert rv.status == '400 BAD REQUEST'


def test_insert_ticket(app, client):
    """
    Insert a new ticket.
    """
    usr = create_user(app, 11188936)
    c = create_course(app, uuid.uuid4())
    link_student_to_course(usr, c)
    link_ta_to_course(usr, c)
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
    usr = create_user(app, 11188936)
    auth = login(client, 11188936)
    c = create_course(app, uuid.uuid4(), students=[usr], supervisors=[usr])
    rv = client.get('/api/courses',
                    headers={'Authorization': auth})
    cid = c.id
    rv = client.post('/api/ticket/submit', json={
        'subject': 'test ticket',
        'message': 'Test bericht',
        'courseid': cid,
        'labelid': ''
    }, headers={
        'Authorization': auth
    })
    rv = client.get('/api/courses',
                    headers={'Authorization': auth})
    cid = c.id
    tickets = client.get('/api/courses/{}/tickets'.format(cid),
                         headers={'Authorization': auth})
    print(tickets.get_json())
    assert len(tickets.get_json()['json_data']) == 1
    ticketid = tickets.get_json()['json_data'][0]['id']
    assert ticketid is not None
