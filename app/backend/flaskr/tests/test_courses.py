from flaskr.tests.utils import create_course, create_user, \
    create_ticket, link_ta_to_course, login
import uuid


def test_get_single_course(app, client):
    """
    Test the api call to get a single course
    """
    create_user(app, 1234)
    courseId = uuid.uuid4()

    create_course(app, courseId)

    rv = client.get('/api/courses/single/{}'.format(courseId))
    json_data = rv.get_json()
    print(json_data)
    assert len(json_data['json_data']) > 0
    assert rv.status == '200 OK'


def test_get_course_tickets(app, client):
    """
    Test the api call to get all tickets belonging to this course
    """

    usr = create_user(app, 1234)
    auth = login(client, 1234)
    ticketId = uuid.uuid4()
    ticketId2 = uuid.uuid4()
    ticketId3 = uuid.uuid4()

    courseId = uuid.uuid4()
    courseId2 = uuid.uuid4()

    create_course(app, courseId, tas=[usr])
    create_course(app, courseId2, tas=[usr])

    create_ticket(app, ticketId, 1234, courseId)
    create_ticket(app, ticketId2, 1234, courseId)
    create_ticket(app, ticketId3, 1234, courseId2)

    rv = client.get('/api/courses/{}/tickets'.format(courseId),
                    headers={
                        'Authorization': auth
                    })

    json_data = rv.get_json()
    print(json_data)
    assert len(json_data['json_data']) == 2
    assert rv.status == "200 OK"

    rv2 = client.get('/api/courses/{}/tickets'.format(courseId2),
                     headers={
                         'Authorization': auth
                     })

    json_data2 = rv2.get_json()
    print(json_data2)
    assert len(json_data2['json_data']) == 1
    assert rv2.status == "200 OK"


def test_get_course_tickets_empty(app, client):
    """
    Database should be empty so no tickets should be returned.
    """
    user = create_user(app, 1234)
    auth = login(client, user.id)
    course = create_course(app, uuid.uuid4(), tas=[user])
    tickets = client.get('/api/courses/{}/tickets'.format(course.id),
                         headers={
                         'Authorization': auth
                         })

    assert tickets.status == '200 OK'
    print(tickets.get_json())
    assert len(tickets.get_json()['json_data']) == 0


def test_create_new_course(app, client):
    """
    Test the api call to create a new course
    """
    create_user(app, 1234)
    auth = login(client, 1234)

    mail = "test@test.com"
    title = "test course title"
    description = "test course description"
    rv = client.post('/api/courses', json={
        "mail": mail,
        "title": title,
        "description": description
    }, headers={
        'Authorization': auth
    })
    assert rv.status == "200 OK"

    rv2 = client.get('/api/courses')
    json_data = rv2.get_json()
    print(json_data)
    assert len(json_data['json_data']) > 0
    found = False
    for course in json_data['json_data']:
        if(course['course_email'] == mail and
                course['title'] == title and
                course['description'] == description):
            found = True
    assert found
    assert rv2.status == '200 OK'


def test_get_all_courses(app, client):
    create_user(app, 1234)

    courseId = uuid.uuid4()
    courseId2 = uuid.uuid4()

    create_course(app, courseId)
    create_course(app, courseId2)

    rv = client.get('/api/courses')
    json_data = rv.get_json()
    print(json_data)
    assert len(json_data['json_data']) >= 2
    assert rv.status == '200 OK'


def test_get_course_tas(app, client):
    user = create_user(app, 1234)
    user2 = create_user(app, 4321)

    courseId = uuid.uuid4()
    course = create_course(app, courseId)
    link_ta_to_course(user, course)
    link_ta_to_course(user2, course)

    rv = client.get('/api/courses/{}/tas'.format(courseId))
    json_data = rv.get_json()
    print(json_data)
    assert rv.status == '200 OK'
    assert len(json_data['json_data']) == 2
