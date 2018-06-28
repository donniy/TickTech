from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from flaskr.config import Config

db = SQLAlchemy()


def init_db():
    """
    Function that initializes the database.
    Moslty just creating the database, but
    if debugging, also populating the database.
    """
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


def deleteSafelyFromDB(item, func=None):
    """
    Function that deletes an item safely from the db.
    If the deletion gives an error, we rollback the session
    and log the database error.
    """
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as err:
        log_database_error(err, func)
        db.session.rollback()
        return False
    return True


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


def addItemSafelyToDB(item, func=None):
    """
    Adds an item to the database.
    If an error happened, we log the error and rollback
    the session. On error we return True, else False.
    """
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as err:
        log_database_error(err, func)
        db.session.rollback()
        return False
    return True


# These are from the InitDB sql file. Can insert dummy data here.
def populate_database_dummy_data():
    """
    This is a function that can be used to populate the database
    with some dummy data. So only be used in debugging.
    """
    from flaskr.models import Course, user, Label

    print("Inserting dummy data")

    items = []

    user1 = user.User()
    user1.create(12345678,"Erik","erik@a.a", "1")

    user2 = user.User()
    user2.create(87654321,"Kire","kire@a.a","1")

    user3 = user.User()
    user3.create(10203040, "student1","studend1@a.a","1")

    user4 = user.User()
    user4.create(50617080, "student2","student2@a.a","1")

    user5 = user.User()
    user5.create(50627080, "Test McTestie","a@a.a","1")

    user6 = user.User()
    user6.create(50637080, "EK","b@b.b","1")

    user7 = user.User()
    user7.create(10000, "Supervisor","super@visor.nl","1")

    # !IMPORTANT! This is for the mail server - ask phtephan
    mail_server = user.User()
    mail_server.create(107584259, "Mail server", "uvapsetest@gmail.com", "NotNull")

    course1 = Course.Course()
    course1.create(uuid.UUID('71d929a86b1311e8adc0fa7ae01bbebc'),"Project Software Engineering","this is a test description",Config.EMAIL_FETCH_EMAIL,"pop.gmail.com","955",Config.EMAIL_FETCH_PASSWORD)

    course2 = Course.Course()
    course2.create(uuid.UUID('51d929a86b1311e8adc0fa7ae01bbebc'),"Operating Systems","this is a test description 2","test@test.com","","","")

    course3 = Course.Course()
    course3.create(uuid.UUID('31d929a86b1311e8adc0fa7ae01bbebc'),"Compiler Construction","this is a test description 3","test2@test.com","","","")

    label1 = Label.Label()
    label1.create(uuid.UUID("fa1b7b20307e4250b59c6d0811315203"), "PSE questions")

    items = [user1, user2, user3, user4, user5, user6, user7, mail_server, course1, course2, course3, label1]

    for item in items:
        addItemSafelyToDB(item, populate_database_dummy_data)
        ("Inserted dummy objects")

    try:
        course1.ta_courses.append(user6)
        course2.ta_courses.append(user6)
        course1.ta_courses.append(user2)
        course3.ta_courses.append(user2)
        course1.ta_courses.append(user1)

        course2.student_courses.append(user1)
        course1.student_courses.append(user3)
        course1.student_courses.append(user5)
        course3.student_courses.append(user5)
        course1.student_courses.append(user4)
        course3.student_courses.append(user3)
        course2.student_courses.append(user4)

        course1.supervisors.append(user7)
        course2.supervisors.append(user7)
        course3.supervisors.append(user7)

        course1.labels.append(label1)
        user6.labels.append(label1)
        db.session.commit()
        print("Inserted dummy links")

    except Exception as exp:
        db.session.rollback()
        log_database_error(exp, populate_database_dummy_data)


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
