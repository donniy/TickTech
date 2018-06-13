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
    print(courseId)
    create_ticket(app, id1, 12345678, courseId)
    create_ticket(app, id2, 12345678, courseId)

    auth = login(client, 1234)

    rv = client.get('/api/user/{}/tickets'.format(12345678),
                    headers={'Authorization': auth})
    json_data = rv.get_json()
    assert rv.status == '200 OK'
    assert len(json_data['json_list']) > 0
    print(json_data['json_list'])

def create_user(app, id):
    new_user = User()
    new_user.id = id
    new_user.name = "test"
    new_user.email = "test@mail.com"
    with app.app_context():
        database.addItemSafelyToDB(new_user)


def create_ticket(app, ticketId, userId, courseId):
    # ticket = Ticket(id=ticketId, user_id=userId, course_id=courseId,
    #                 status_id=1, title="sub", email="mail@mail.com",
    #                 timestamp=datetime.now())
    t = Ticket()
    t.id = ticketId
    t.user_id = userId
    t.course_id = courseId
    t.status_id = 1
    t.email = "mail@mail.com"
    t.title = "title"
    t.timestamp = datetime.now()
    with app.app_context():
        database.addItemSafelyToDB(t)


def create_course(app, courseId):
    course = Course()
    course.id = courseId
    course.course_email = "mail@mail.com"
    course.title = "test_title"
    course.description = "desc"
    with app.app_context():
        database.addItemSafelyToDB(course)


def login(client, userId):
    login = client.post('/auth', json={
        'username': userId,
        'password': "random"
    })
    token = login.get_json()
    return 'JWT '+token['access_token']

    # return {'Authorization': 'JWT '+token['access_token']}
