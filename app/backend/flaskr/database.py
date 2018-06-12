from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os.path
from sqlalchemy_utils import UUIDType
import uuid

db = SQLAlchemy()

class DatabaseException(Exception):
    def __init__(self, debug_message):
        self.debug_message = debug_message

class DatabaseInsertException(DatabaseException):
    def __init__(self, debug_message):
        super().__init__(debug_message)
        self.response_message = response_message = ""

def init_db():
    db.create_all()
    populate_database_dummy_data()
    addTicketStatus()
    addTicketStatus("closed")
    addTicket()

def get_db():
    return db

def serialize_list(l):
    return [i.serialize for i in l]

def json_list(l):
    """
    Maak JSON van de lijst.
    """
    return jsonify(json_list=serialize_list(l))


# Use these functions if you want to add items to
# to the database.
def addItemSafelyToDB(item):
    """
    Add the item to the db by checking
    if the item is valid. The error can be logged.
    """
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as err:
        print("Logging database error: {0}".format(err))
        db.session.rollback()
        return False
    return True


#end functions for insertion for database.

#These are from the InitDB sql file. Can insert dummy data here.
def populate_database_dummy_data():
    from flaskr.models import Course, user
    items = []
    course = Course.Course(id=uuid.uuid4(), course_email="test@test.com",
                           title="course 1", description="Test")
    course2 = Course.Course(id=uuid.uuid4(), course_email="testie@test.com",
                            title="course 2", description="Test")
    user1 = user.User(id=11111, name="Erik Kooijstra", email="Erik@kooijstra.nl")
    user2 = user.User(id=11112, name="Kire Kooijstra", email="Kire@kooijstra.nl")
    user3 = user.User(id=123123123, name="Test mctestie", email="test@test.nl")
    items = [user1, user2, user3, course, course2]
    for item in items:
        addItemSafelyToDB(item)

    try:
        course.student_courses.append(user3)
        course2.student_courses.append(user3)
        course.ta_courses.append(user1)
        course2.ta_courses.append(user2)
    except Exception as exp:
        db.session.rollback()
        print(exp)

    print(course.student_courses)
    print(course.ta_courses)

#just for testing
def addTicketStatus(name="Needs help"):
    from flaskr.models import ticket
    ts = ticket.TicketStatus()
    ts.name = name
    try:
        addItemSafelyToDB(ts)
    except:
        print("oeps")

def addTicketLabel(ticked_id=1, course_id="1", name="test"):
    from flaskr.models import ticket
    tl = ticket.TicketLabel()
    tl.ticked_id = ticked_id
    tl.course_id = course_id
    tl.name = name
    try:
        addItemSafelyToDB(tl)
    except:
        print("oeps")

#just for testing
def addTicket(user_id=1, email="test@email.com", course_id="1", status_id=2, title="test",
              timestamp=datetime.now()):
    from flaskr.models import ticket
    t = ticket.Ticket()
    t.id = uuid.uuid1()
    addTicketLabel(t.id, course_id, title)
    t.user_id = user_id
    t.email = email
    t.course_id = course_id
    t.status_id = 10000
    t.title = title
    t.timestamp = timestamp
    t.label_id = 1
    try:
        addItemSafelyToDB(t)
    except DatabaseInsertException as exp:
        print(exp.response_message)
