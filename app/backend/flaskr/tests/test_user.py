from flaskr.tests.utils import create_user, create_course, \
    create_ticket, login
import uuid


def test_get_user(app, client):
    """
    Test the api call to get one user.
    """

    create_user(app, 1234)

    rv = client.get('/api/user/{}'.format(1234))
    json_data = rv.get_json()
    assert rv.status == '200 OK'
    print("call returned:")
    print(json_data['json_data'])
    assert len(json_data['json_data']) > 0


def test_get_user_tickets(app, client):
    """
    Test the api call to get the tickets of one users
    """

    create_user(app, 1234)

    id1 = uuid.uuid4()
    id2 = uuid.uuid4()
    courseId = uuid.uuid4()

    create_course(app, courseId)
    create_ticket(app, id1, 1234, courseId)
    create_ticket(app, id2, 1234, courseId)

    auth = login(client, 1234)

    rv = client.get('/api/user/{}/tickets'.format(1234),
                    headers={'Authorization': auth})
    json_data = rv.get_json()
    assert rv.status == '200 OK'
    assert len(json_data['json_data']) > 0
    print(json_data['json_data'])


def test_get_active_student_tickets(app, client):
    create_user(app, 1234)
    id1 = uuid.uuid4()
    id2 = uuid.uuid4()
    courseId = uuid.uuid4()

    create_course(app, courseId)
    create_ticket(app, id1, 1234, courseId, 1)
    create_ticket(app, id2, 1234, courseId, 2)

    auth = login(client, 1234)
    rv = client.get('/api/user/{}/tickets/active'.format(1234),
                    headers={'Authorization': auth})
    rv2 = client.get('/api/user/{}/tickets'.format(1234),
                     headers={'Authorization': auth})

    active_tickets = rv.get_json()['json_data']
    all_tickets = rv2.get_json()['json_data']
    assert rv.status == '200 OK'
    assert len(active_tickets) > 0
    assert len(all_tickets) - len(active_tickets) == 1
    assert len(all_tickets) != len(active_tickets)


def test_get_student_courses(app, client):
    user = create_user(app, 1234)
    courseId = uuid.uuid4()
    create_course(app, courseId, [], [user])
    rv = client.get('/api/user/{}/courses'.format(1234))
    json_data = rv.get_json()
    print(json_data)
    assert rv.status == "200 OK"
    assert len(json_data['json_data']) > 0


def test_user_auth(app, client):
    create_user(app, 1234)
    id1 = uuid.uuid4()
    id2 = uuid.uuid4()
    courseId = uuid.uuid4()

    create_course(app, courseId)
    create_ticket(app, id1, 1234, courseId, 1)
    create_ticket(app, id2, 1234, courseId, 2)

    rv = client.get('/api/user/{}/tickets/active'.format(1234))
    rv2 = client.get('/api/user/{}/tickets'.format(1234))
    rv3 = client.get('/api/user/{}/tickets'.format(1234),
                     headers={'Authorization': ""})

    print(rv.status)
    print(rv2.status)
    print(rv3.status)
    assert rv.status == "401 UNAUTHORIZED"
    assert rv2.status == "401 UNAUTHORIZED"
    assert rv3.status == "401 UNAUTHORIZED"
