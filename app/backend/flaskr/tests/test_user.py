import pytest
import json
from flaskr.database import get_db
from flaskr.models.user import *
from flaskr.models.ticket import *


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
    assert len(json_data['json_list']) > 0
    print(json_data['json_list'])


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

    active_tickets = rv.get_json()['json_list']
    all_tickets = rv2.get_json()['json_list']
    assert rv.status == '200 OK'
    assert len(active_tickets) > 0
    assert len(all_tickets) - len(active_tickets) == 1
    assert len(all_tickets) != len(active_tickets)


def test_get_student_courses(app, client):
    user = create_user(app, 1234)
    courseId = uuid.uuid4()
    course = create_course(app, courseId, [], [user])
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

    auth = login(client, 1234)
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


# helper functions
def create_user(app, id):
    new_user = User()
    new_user.id = id
    new_user.name = "test"
    new_user.email = "test@mail.com"
    database.addItemSafelyToDB(new_user)
    return new_user


def create_ticket(app, ticketId, userId, courseId, status=1):
    # ticket = Ticket(id=ticketId, user_id=userId, course_id=courseId,
    #                 status_id=1, title="sub", email="mail@mail.com",
    #                 timestamp=datetime.now())
    t = Ticket()
    t.id = ticketId
    t.user_id = userId
    t.course_id = courseId
    t.status_id = status
    t.email = "mail@mail.com"
    t.title = "title"
    t.timestamp = datetime.now()
    with app.app_context():
        database.addItemSafelyToDB(t)
    return t


def create_course(app, courseId, tas=[], students=[]):
    course = Course()
    course.id = courseId
    course.course_email = "mail@mail.com"
    course.title = "test_title"
    course.description = "desc"
    course.ta_courses = tas
    course.student_courses = students
    with app.app_context():
        database.addItemSafelyToDB(course)
    return course


def link_ta_to_course(user, course):
    course.ta_courses.append(user)


def login(client, userId):
    login = client.post('/auth', json={
        'username': userId,
        'password': "random"
    })
    token = login.get_json()
    return 'JWT '+token['access_token']

    # return {'Authorization': 'JWT '+token['access_token']}
