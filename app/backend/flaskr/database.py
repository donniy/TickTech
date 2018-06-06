from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os.path


db = SQLAlchemy()

def init_db():
    db.create_all()
    addTicketStatus()
    addTicket()


def json_list(l):
    """
    Maak JSON van de lijst.
    """
    return jsonify(json_list=[i.serialize for i in l])


# Use these functions if you want to add items to
# to the database.
def addListSafelyToDB(items):
    """
    Add a list of items safely to the database
    by checking if the item is valid.
    If an item is not valid it will be discarded/
    """
    succes = []
    for item in items:
        try:
            print(item)
            item.checkValid
            db.session.add(item)
            succes += [True]
        except ValueError as err:
            print(err)
            succes += [False]
    db.session.commit()
    return succes


def addItemSafelyToDB(item):
    """
    Add the item to the db by checking
    if the item is valid. The error can be logged.
    """
    return addListSafelyToDB([item])

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
    t.status_id = 1
    t.title = title
    t.timestamp = timestamp
    t.label_id = 1
    succes = addItemSafelyToDB(t)
    print(succes)

def addNote(user_id=1, ticket_id=1,text="", timestamp=datetime.now()):
    from flaskr.models import Note
    n = Note.Note()
    n.user_id = user_id
    n.ticket_id = ticket_id
    n.text = text
    n.timestamp = timestamp
    success = addItemSafelyToDB(n)
    print(success)