from flaskr import database
from flaskr.models.user import *
from flaskr.models.ticket import *
from flaskr.models.Note import *


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
    database.addItemSafelyToDB(course)
    return course


def create_note(app, noteId, ticketId, userId, text):
    note = Note()
    note.id = noteId
    note.ticket_id = ticketId
    note.user_id = userId
    note.text = text
    database.addItemSafelyToDB(note)
    return note


def link_ta_to_course(user, course):
    course.ta_courses.append(user)


def login(client, userId):
    login = client.post('/auth', json={
        'username': userId,
        'password': "random"
    })
    token = login.get_json()
    return 'JWT '+token['access_token']
