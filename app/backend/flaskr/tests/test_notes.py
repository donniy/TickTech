import pytest
import json
from flaskr.database import get_db
from flaskr.tests.utils import *


def test_get_ticket_notes(app, client):
    """
    Test the api call to get all notes belonging to a ticket
    """
    create_user(app, 1234)
    ticketId = uuid.uuid4()
    ticketId2 = uuid.uuid4()
    courseId = uuid.uuid4()

    create_course(app, courseId)
    create_ticket(app, ticketId, 1234, courseId)
    create_ticket(app, ticketId2, 1234, courseId)

    noteId1 = uuid.uuid4()
    noteId2 = uuid.uuid4()
    noteId3 = uuid.uuid4()
    create_note(app, noteId1, ticketId, 1234, "dit is een test bericht")
    create_note(app, noteId2, ticketId, 1234, "dit is een test bericht2")
    create_note(app, noteId3, ticketId2, 1234, "deze zou je niet moeten zien")

    rv = client.get('/api/notes/{}'.format(ticketId))
    json_data = rv.get_json()
    print(json_data)
    assert len(json_data['json_data']) == 2
    assert rv.status == '200 OK'


def test_add_new_note(app, client):
    """
    Test the api call to add a new note to a ticket
    """
    create_user(app, 1234)
    courseId = uuid.uuid4()
    create_course(app, courseId)
    ticketId = uuid.uuid4()
    create_ticket(app, ticketId, 1234, courseId)

    auth = login(client, 1234)

    rv = client.post('/api/notes', json={
        "ticket_id": ticketId,
        "user_id": 1234,
        "text": "dit is een test notitie"
    }, headers={
        'Authorization': auth
    })
    assert rv.status == '201 CREATED'

    rv2 = client.get('/api/notes/{}'.format(ticketId))
    json_data = rv2.get_json()
    print(json_data)
    assert len(json_data['json_data']) == 1
    assert rv2.status == '200 OK'


def test_remove_note(app, client):
    """
    Test the api call to remove a note
    """
    create_user(app, 1234)
    courseId = uuid.uuid4()
    create_course(app, courseId)
    ticketId = uuid.uuid4()
    create_ticket(app, ticketId, 1234, courseId)

    noteId1 = uuid.uuid4()
    noteId2 = uuid.uuid4()
    create_note(app, noteId1, ticketId, 1234, "dit is een test bericht")
    create_note(app, noteId2, ticketId, 1234, "dit is een test bericht2")

    auth = login(client, 1234)
    rv = client.post('/api/notes/{}/close'.format(noteId1),
                     headers={'Authorization': auth}
                     )

    json_data = rv.get_json()
    assert rv.status == "202 ACCEPTED"

    rv2 = client.get('/api/notes/{}'.format(ticketId))
    json_data = rv2.get_json()
    print(json_data)
    assert len(json_data['json_data']) == 1
