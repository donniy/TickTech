from flaskr import database
from flaskr.models.user import User
from flaskr.models.ticket import Ticket
from flaskr.models.Note import Note
from flaskr.models.Course import Course
from datetime import datetime


def create_user(app, id):
    new_user = User()
    new_user.id = id
    new_user.name = "test"
    new_user.email = "test@mail.com"
    database.addItemSafelyToDB(new_user)
    return new_user


def create_ticket(app, ticketId, userId, courseId, status=1):
    ticket = Ticket()
    ticket.id = ticketId
    ticket.user_id = userId
    ticket.course_id = courseId
    ticket.status_id = status
    ticket.email = "mail@mail.com"
    ticket.title = "title"
    ticket.timestamp = datetime.now()
    database.addItemSafelyToDB(ticket)
    return ticket


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


def link_student_to_course(user, course):
    course.student_courses.append(user)


def link_ta_to_ticket(user, ticket):
    ticket.bound_tas.append(user)


def login(client, userId):
    login = client.post('/auth', json={
        'username': userId,
        'password': "random"
    })
    token = login.get_json()
    return 'JWT '+token['access_token']
