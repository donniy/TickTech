from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os.path


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
    addTicketStatus()
    addTicketStatus("closed")
    addTicket()


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
        item.checkValid
    except DatabaseException as DBerror:
        print("DEBUG: " + DBerror.debug_message)
        raise DBerror
    db.session.add(item)
    db.session.commit()


#end functions for insertion for database.

#just for testing
def addTicketStatus(name="Needs help"):
    from flaskr.models import ticket
    ts = ticket.TicketStatus()
    ts.name = name
    addItemSafelyToDB(ts)


def addTicketLabel(ticked_id=1, course_id="1", name="test"):
    from flaskr.models import ticket
    tl = ticket.TicketLabel()
    tl.ticked_id = ticked_id
    tl.course_id = course_id
    tl.name = name
    addItemSafelyToDB(tl)


#just for testing
def addTicket(user_id=1, email="test@email.com", course_id="1", status_id=1, title="test",
              timestamp=datetime.now()):
    from flaskr.models import ticket
    t = ticket.Ticket()
    addTicketLabel(t.id, course_id, title)
    t.user_id = user_id
    t.email = email
    t.course_id = course_id
    t.status_id = 10000
    t.title = title
    t.timestamp = timestamp
    t.label_id = 1
    try:
        success = addItemSafelyToDB(t)
        print(success)
    except DatabaseInsertException as exp:
        print(exp.response_message)

def addNote(user_id=1, ticket_id=1,text="", timestamp=datetime.now()):
    from flaskr.models import Note
    n = Note.Note()
    n.user_id = user_id
    n.ticket_id = ticket_id
    n.text = text
    n.timestamp = timestamp
    try:
        success = addItemSafelyToDB(n)
        print(success)
    except DatabaseInsertException as exp:
        print(exp)

        
