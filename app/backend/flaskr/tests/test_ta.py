from flaskr.tests.utils import create_user, create_course, \
    link_ta_to_course, link_student_to_course, link_ta_to_ticket, \
    create_ticket, login
import uuid


def test_get_ta_tickets(app, client):
    """
    Test the api call to get one user.
    """
    taId = 1234
    student = 4321
    ta = create_user(app, taId)
    usr = create_user(app, student)

    courseId1 = uuid.uuid4()
    courseId2 = uuid.uuid4()
    course1 = create_course(app, courseId1)
    course2 = create_course(app, courseId2)

    link_ta_to_course(ta, course1)
    link_student_to_course(ta, course2)

    auth = login(client, ta.id)

    ticketId1 = uuid.uuid4()
    ticketId2 = uuid.uuid4()
    # create ticket in course where TA
    ticket1 = create_ticket(app, ticketId1, taId, courseId1)
    link_ta_to_ticket(ta, ticket1)
    # create ticket in course where not TA
    create_ticket(app, ticketId2, taId, courseId2)

    rv = client.get('/api/ta/{}/tickets'.format(taId),
                    headers={'Authorization': auth})
    json_data = rv.get_json()['json_data']
    assert rv.status == '200 OK'
    print(json_data)
    assert len(json_data) == 1
    print(json_data[0]['tas'])
    assert len(json_data[0]['tas']) == 1
    assert json_data[0]['tas'][0]['id'] == taId

# TODO add @apiBluePrint.route('/ta/<user_id>/courses')
