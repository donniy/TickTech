from flaskr.tests.utils import create_user, login, create_course, create_ticket
import uuid


def test_insert_ticket(app, client):
    """
    Insert a new ticket.
    """
    userId = 11188936
    create_user(app, userId)
    auth = login(client, userId)
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
    userId = 11188936
    userId2 = 11037383
    create_user(app, userId)
    user = create_user(app, userId2)
    courseid = uuid.uuid4()
    course = create_course(app, courseid, tas=[user])
    auth = login(client, userId)
    auth2 = login(client, userId2)
    rv = client.post('/api/ticket/submit', json={
        'subject': 'test ticket',
        'message': 'Test bericht',
        'courseid': courseid,
        'labelid': ''
    }, headers={
        'Authorization': auth
    })
    tickets = client.get('/api/courses/{}/tickets'.format(courseid),
                         headers={
                             'Authorization': auth2
                         })

    assert len(tickets.get_json()['json_data']) == 1
    ticketid = tickets.get_json()['json_data'][0]['id']
    assert ticketid is not None


def test_close_ticket(app, client):
    """
        Close a ticket
    """
    userId = 1234
    user = create_user(app, userId)

    courseId = uuid.uuid4()
    create_course(app, courseId, tas=[user])

    ticketId1 = uuid.uuid4()
    ticketId2 = uuid.uuid4()
    create_ticket(app, ticketId1, userId, courseId)
    create_ticket(app, ticketId2, userId, courseId)

    auth = login(client, userId)

    rv = client.post('/api/ticket/{}/close'.format(ticketId1),
                     headers={'Authorization': auth}
                     )

    json_data = rv.get_json()
    assert rv.status == "200 OK"
    print(json_data)

    rv2 = client.get('/api/courses/{}/tickets'.format(courseId),
                     headers={'Authorization': auth})

    json_data2 = rv2.get_json()

    accepted = False
    for x in json_data2['json_data']:
        if(x['id'] == str(ticketId1) and x['status']['id'] == 2):
            accepted = True
        if(x['id'] == str(ticketId2) and x['status']['id'] == 2):
            accepted = False
            break

    assert accepted
    assert len(json_data2['json_data']) == 2
    assert rv2.status == "200 OK"


def test_add_message_to_ticket(app, client):
    """
        Add message to existing ticket
    """
    userId = 1234
    testMessage = "this is a test message"
    create_user(app, userId)

    courseId = uuid.uuid4()
    create_course(app, courseId)

    ticketId = uuid.uuid4()
    create_ticket(app, ticketId, userId, courseId)

    auth = login(client, userId)

    rv = client.post('/api/ticket/{}/messages'.format(ticketId),
                     json={'message': testMessage,
                           'user_id': userId},
                     headers={'Authorization': auth}
                     )
    json_data = rv.get_json()
    assert rv.status == "201 CREATED"
    assert len(json_data) > 0
    print(json_data)

    rv2 = client.get('/api/ticket/{}/messages'.format(ticketId),
                     headers={'Authorization': auth})
    assert rv2.status == '200 OK'
    json_data = rv2.get_json()
    assert json_data['json_data'][0]['text'] == testMessage
    assert json_data['json_data'][0]['user_id'] == userId
    assert len(json_data['json_data']) == 1
    print(rv2.get_json())


def test_get_ticket_messages(app, client):
    """
        Get messages which belong to a ticket
    """
    userId1 = 1234
    userId2 = 4321
    testMessage1 = "this is a test message1"
    testMessage2 = "this is a test message2"
    create_user(app, userId1)
    create_user(app, userId2)

    courseId = uuid.uuid4()
    create_course(app, courseId)

    ticketId = uuid.uuid4()
    create_ticket(app, ticketId, userId1, courseId)

    auth1 = login(client, userId1)
    auth2 = login(client, userId2)

    client.post('/api/ticket/{}/messages'.format(ticketId),
                json={'message': testMessage1,
                      'user_id': userId1},
                headers={'Authorization': auth1}
                )
    client.post('/api/ticket/{}/messages'.format(ticketId),
                json={'message': testMessage2,
                      'user_id': userId2},
                headers={'Authorization': auth2}
                )

    rv2 = client.get('/api/ticket/{}/messages'.format(ticketId),
                     headers={'Authorization': auth1})
    assert rv2.status == '200 OK'
    json_data = rv2.get_json()
    assert json_data['json_data'][0]['text'] == testMessage1
    assert json_data['json_data'][0]['user_id'] == userId1
    assert json_data['json_data'][1]['text'] == testMessage2
    assert json_data['json_data'][1]['user_id'] == userId2
    assert len(json_data['json_data']) == 2
    print(rv2.get_json())


def test_ticket_file_download(app, client):
    """
        Download a file
    """
    # TODO to be filled in by RensiePensie
