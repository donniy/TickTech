from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from flaskr.config import Config

db = SQLAlchemy()


def init_db():
    db.create_all()
    populate_database_dummy_data()
    addTicketStatus("Unassigned")
    addTicketStatus("Closed")
    addTicketStatus("Assigned but waiting for reply")
    addTicketStatus("Receiving help")
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


def log_database_error(err, func=None):
    """
    Function that logs the database error.
    This functions prints the database error to stdout
    and if a function is specified, the name of the functions
    and the module where the function is found
    will be printed to stdout.
    __getframe is not used, because it is not
    guaranteed to exist.
    """
    import sys
    print("-" * 36 + "database" + "-" * 36)
    print("Error when adding an item to the database")
    print("The error is:")
    print(err)
    if func is not None:
        print("The name of the caller is:")
        print(func.__name__)
        print("This function can be found in the module:")
        print(func.__module__)
    print("-" * 80)
    print()


def commitSafelyToDB(func=None):
    """
    Function that commits the current database.
    If an error is found we log the error
    and the session will be rolled back,
    so the commit has not taken place.
    Returns True if the commit was succesful
    False if not.
    """
    try:
        db.session.commit()
    except Exception as err:
        log_database_error(err, func)
        db.session.rollback()
        return False
    return True


# Use these functions if you want to add items to
# to the database.
def addItemSafelyToDB(item, func=None):
    """
    Add the item to the db by checking
    if the item is valid. The error can be logged.
    """
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as err:
        log_database_error(err, func)
        db.session.rollback()
        return False
    return True

# End functions for insertion for database.

# These are from the InitDB sql file. Can insert dummy data here.
def populate_database_dummy_data():
    from flaskr.models import Course, user
    items = []
    course = Course.Course(id=uuid.uuid4(),
                           course_email=Config.EMAIL_FETCH_EMAIL,
                           mail_server_url="pop.gmail.com",
                           mail_port="995",
                           mail_password=Config.EMAIL_FETCH_PASSWORD,
                           title="course 1",
                           description="Test")

    course2 = Course.Course(id=uuid.uuid4(),
                            course_email="testie@test.com",
                            title="course 2",
                            description="Test")

    user1 = user.User(id=11111,
                      name="Erik Kooijstra",
                      email="Erik@kooijstra.nl")

    user2 = user.User(id=11112,
                      name="Kire Kooijstra",
                      email="Kire@kooijstra.nl")

    user3 = user.User(id=123123123,
                      name="Test mctestie",
                      email="test@test.nl")

    user4 = user.User(id=10000,
                      name="Supervisor",
                      email="super@visor.nl")

    user5 = user.User(id=111111111,
                      name="Test test",
                      email="test@test.nl")

    # !IMPORTANT! This is for the mail server - ask stephan
    mail_server = user.User(id=107584259,
                            name="Mail server",
                            email="uvapsetest@gmail.com")

    items = [user1, user2, user3, user5, mail_server, course, course2]

    for item in items:
        addItemSafelyToDB(item, populate_database_dummy_data)

    try:
        course.supervisors.append(user4)
        course2.supervisors.append(user4)
        course.student_courses.append(user3)
        course2.student_courses.append(user3)
        course.student_courses.append(user5)
        course2.student_courses.append(user5)
        course.ta_courses.append(user1)
        course2.ta_courses.append(user2)
    except Exception as exp:
        db.session.rollback()
        log_database_error(exp, populate_database_dummy_data)

    print(course.student_courses)
    print(course.ta_courses)



# Just for testing
def addTicketStatus(name="Needs help"):
    from flaskr.models import ticket
    ts = ticket.TicketStatus()
    ts.name = name
    try:
        addItemSafelyToDB(ts, addTicketStatus)
    except Exception as e:
        print(e)


def addTicketLabel(ticked_id=uuid.uuid4(), course_id=uuid.uuid4(),
                   name="test"):
    from flaskr.models import ticket
    tl = ticket.TicketLabel()
    tl.ticked_id = ticked_id
    tl.course_id = course_id
    tl.name = name
    try:
        addItemSafelyToDB(tl, addTicketLabel)
    except Exception as e:
        print(e)


def addTicket(user_id=1, email="test@email.com", course_id=uuid.uuid4(),
              status_id=2, title="test",
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
    t.label_id = uuid.uuid4()
    try:
        addItemSafelyToDB(t, addTicket)
    except DatabaseInsertException as exp:
        print(exp.response_message)
